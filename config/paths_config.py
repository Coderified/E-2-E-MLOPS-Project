#will list all the paths 

import os


#PAths for data ingestion
# we wannt to store data in 'raw' folder in artifacts

RAW_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DIR,"raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR,"train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR,"test.csv")

#path to config yaml
CONFIG_PATH = "config/config.yaml"


#Paths for DataProcessing
PROCESSED_DIR = "artifacts/processed"
PROCESSED_TRAIN_FILE_PATH = os.path.join(PROCESSED_DIR,"proc_train.csv")
PROCESSED_TEST_FILE_PATH = os.path.join(PROCESSED_DIR,"proc_test.csv")


## MODEL TRAINING

MODEL_OUTPUT_PATH = "artifacts/models/lightgbm.pkl"

    