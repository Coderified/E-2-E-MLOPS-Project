import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException

#all paths get imported here
from config.paths_config import *
from utils.common_functions import read_yaml,load_data

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

#initialize logger
logger = get_logger(__name__)

class DataProcessor:

    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config = read_yaml(config_path)  #config here is the config.yaml file defined under config
        
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self,df):
        try:
            logger.info("Starting data processing")

            logger.info("Dropping columns")

            df.drop(['Unnamed: 0',"Booking_ID"],axis=1,inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info("Applying Label Encoding")
            le=LabelEncoder()

            lemapping={}

            for cols in cat_cols:
                df[cols] = le.fit_transform(df[cols])
                lemapping[cols] = {label:code for label,code in zip(le.classes_,le.transform(le.classes_))}

            logger.info(f"Label mappings are:")
            for col,mappin in lemapping.items():
                logger.info(f"{col} : {mappin}")

            logger.info("Handling Skews")

            skew_threshold = self.config['data_processing']["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x:x.skew())

            for cols in skewness[skewness>skew_threshold].index:
                df[cols]=np.log1p(df[cols])

            return df
        
        except Exception as e:
            logger.error("Error in preprocess :{e}")

            raise CustomException("Error while preprocess data",e)
        
    def balance_data(self,df):
        try:
            logger.info("Handling Imbalance")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            smote = SMOTE()
            X_res , y_res = smote.fit_resample(X,y)
            bal_df = pd.DataFrame(X_res,columns=X.columns)
            bal_df["booking_status"]=y_res
            df1= bal_df.copy()

            logger.info("Balancing Completed")
            return df1
        
        except Exception as e:
            logger.error("Error in Balancing :{e}")

            raise CustomException("Error while Balancing data",e)
        
    def feature_selection(self,df):
        try:
            logger.info("Beg Feat Selection")
            X=df.drop("booking_status",axis=1)
            y=df["booking_status"]

            model =  RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance = model.feature_importances_
            feat_imp_df = pd.DataFrame({
                'features':X.columns,
                'feature_importances':feature_importance
            })
            feat_imp_df = feat_imp_df.sort_values(by="feature_importances",ascending=False)
            top_10_feats = feat_imp_df.head(10)
            top_10_feat_cols = list(top_10_feats['features'])

            top_10_df = df[top_10_feat_cols + ["booking_status"]]

            logger.info("Feature Selection Done")

            return top_10_df
        
        except Exception as e:
            logger.error("Error in Feat Selection :{e}")

            raise CustomException("Error while Feat Selection",e)
        
    def save_data(self,df,save_path):
        try:
            logger.info("Saving data in processed folder")
            df.to_csv(save_path,index=False)
            logger.info(f"Data saved successfully to {save_path}")
        except Exception as e:
            logger.error("Error in Saving preproc data :{e}")

            raise CustomException("Error while saving preproc data",e)
        
    def process(self):
        try:
            logger.info("Loading Data from Raw")
            
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)
            
            train_df = self.feature_selection(train_df)
            test_df = test_df[train_df.columns] #selecting only features of top 10 in train

            self.save_data(train_df,PROCESSED_TRAIN_FILE_PATH)
            self.save_data(test_df,PROCESSED_TEST_FILE_PATH)

            logger.info("Data pre Processing and save in PROCESSED FOLDER Completed")


        except Exception as e:
            logger.error("Error in full preproc pipeline :{e}")

            raise CustomException("Error while full preproc pipeline",e)
        
if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()
            
