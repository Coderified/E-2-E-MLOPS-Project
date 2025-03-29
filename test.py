from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def dividenum(a,b):
    try:
        result = a/b
        logger.info("dividing two nos")
        return result
    except Exception as e:
        logger.error("Error")
        raise CustomException("Custom Zero Error",sys)
    
#all things under this block gets executed when this py file is called
if __name__ == '__main__':
    try:
        logger.info("Starting main program")
        dividenum(5,0)
    except CustomException as ce:
        logger.error(str(ce)) 
        
#text representation of error gets logged
