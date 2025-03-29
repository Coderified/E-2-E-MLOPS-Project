import os
import pandas as pd

from google.cloud import storage
from sklearn.model_selection import train_test_split


#import logger &  customer exception
from src.logger import get_logger
from src.custom_exception import CustomException

#all paths get imported here
from config.paths_config import *
from utils.common_functions import read_yaml

#initialize logger
logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]  #config here is the config.yaml file defined under config
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"] 


# under artifacts we store all our files we gonna create under raw folder

        os.makedirs(RAW_DIR,exist_ok=True) #Raw_Dir from paths_config

        logger.info(f"Data Ingestion started with{self.bucket_name} & file name is {self.bucket_file_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"CSV file is succesfully downloaded to{RAW_FILE_PATH}")

        except Exception as e:
            logger.error("Error while dwlding CSV file")
            raise CustomException("Failed to download csv file",e)

    def split_data(self):
        try:
            logger.info("Splitting begins")
            data=pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data,train_size=self.train_test_ratio,random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info("Train and test data saved")

        except Exception as e:
            logger.error("Error while splitting data")
            raise CustomException("Failed to split data",e)


    def run(self):
        try:
            logger.info("Starting data ingestion")
            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data split complete")

        except CustomException as ce:
            logger.error(f"Custom Exception : {str(ce)}")

        finally:
            logger.info("Data Ingestion Completed")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
            










