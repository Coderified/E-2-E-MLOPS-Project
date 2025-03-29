#function for reading yaml files - will happen at multiple times

import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml
import pandas as pd

logger = get_logger(__name__)

#we need to read yaml files

def read_yaml(file_path): #file path is specified in paths_config.py files
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not in the given path")
        
        with open(file_path,'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("YAML Loaded")
            return config
        
    
    except Exception as e:
        logger.error("Error reading the Yaml File")
        raise CustomException("Failed to read Yaml File",e)
    


def load_data(path):
    try:
        logger.info("Loading Data")
        return pd.read_csv(path) 
    except Exception as e:
        logger.error(f"Error loading data {e}")
        raise CustomException("failed to load data",e)
    

    