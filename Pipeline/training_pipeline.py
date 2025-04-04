from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTrainer

from utils.common_functions import read_yaml
from config.paths_config import *

if __name__ == "__main__":
    #Data Ingestion
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

    #Data Preprocessing
    processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()


    #Model_Training
    trainer = ModelTrainer(PROCESSED_TRAIN_FILE_PATH,PROCESSED_TEST_FILE_PATH,MODEL_OUTPUT_PATH)
    trainer.run()
