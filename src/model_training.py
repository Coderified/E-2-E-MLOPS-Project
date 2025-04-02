import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from scipy.stats import randint


from src.logger import get_logger
from src.custom_exception import CustomException

#all paths get imported here
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml,load_data

import mlflow
import mlflow.sklearn

#initialize logger
logger = get_logger(__name__)

class ModelTrainer():
    #here processed train and processed test will be the train and test paths
    def __init__(self,train_path,test_path,model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LGB_PARAMS
        self.random_search_params = RANDOMSEARCH_PARAMS

    def load_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path} & {self.test_path}")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Data splitted successfully for Model Training")
            return X_train,y_train,X_test,y_test
        
        except Exception as e:
            logger.error(f"Error while loading data {e}")
            raise CustomException("Failed to load data" ,  e)
        
    def train_model(self,X_train,y_train):
        try:
            logger.info("Model Initialize")

            lgbm_model = lgb.LGBMClassifier(force_col_wise=True,early_stopping_rounds=50)

            logger.info("Beginning HP tuning")
            
            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter = self.random_search_params["n_iter"],
                n_jobs=self.random_search_params["n_jobs"],
                cv = self.random_search_params["cv"],
                verbose =self.random_search_params["verbose"],
                scoring=self.random_search_params["scoring"],
                refit=True
            ) 

            logger.info("Starting HP tune")

            random_search.fit(X_train,y_train)

            logger.info("HP tuning Done")

            bestparams = random_search.best_params_
            bestmodel = random_search.best_estimator_

            logger.info(f"Best params are {bestparams}")

            return bestmodel
        
        except Exception as e:
            logger.error(f"Error while training model {e}")
            raise CustomException("Failed to train model" ,  e)

    def model_evaluation(self,best_model,X_test,y_test):
        try:

            y_pred = best_model.predict(X_test)

            accuracy = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)

            logger.info(f"Accuracy Score : {accuracy}")
            logger.info(f"Precision Score : {precision}")
            logger.info(f"Recall Score : {recall}")
            logger.info(f"F1 Score : {f1}")

            return {
                "accuracy" : accuracy,
                "precison" : precision,
                "recall" : recall,
                "f1" : f1
            }
        except Exception as e:
            logger.error(f"Error while evaluating model {e}")
            raise CustomException("Failed to evaluate model" ,  e)
        
    def save_model(self,model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path),exist_ok=True)
            logger.info("saving the model")
            joblib.dump(model , self.model_output_path)
            logger.info(f"Model saved to {self.model_output_path}")
        
        except Exception as e:
            logger.error(f"Error while evaluating model {e}")
            raise CustomException("Failed to evaluate model",e)
        
    def run(self):
        try:

            with mlflow.start_run():
                logger.info("Starting model training Pipeline")
                
                logger.info("Starting our MLFLOW experimentation")

                
                logger.info("Logging the training and testing datset to MLFLOW")
                mlflow.log_artifact(self.train_path,artifact_path="datasets")
                mlflow.log_artifact(self.test_path,artifact_path="datasets")

                X_train,y_train,X_test,y_test = self.load_split_data()
                best_lgbm_model = self.train_model(X_train,y_train)
                metrics = self.model_evaluation(best_lgbm_model,X_test,y_test)
                self.save_model(best_lgbm_model)

                logger.info("Logging the model into mlflow")
                mlflow.log_artifact(self.model_output_path)
                
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("Model training done")

        except Exception as e:
            logger.error(f"Error in model training pipeline {e}")
            raise CustomException("Failed during model training pipeline",e)
        
if __name__ == "__main__":
    trainer = ModelTrainer(PROCESSED_TRAIN_FILE_PATH,PROCESSED_TEST_FILE_PATH,MODEL_OUTPUT_PATH)
    trainer.run()
     

            


        

