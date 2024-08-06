import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))
from src.exception import CustomException
from src.logger import lg

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.Components.model_trainer import ModelTrainer
from src.Components.data_transformation import DataTranformationConfig
from src.Components.data_transformation import DataTransformation

@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('artifacts',"train.csv")
    test_data_path:str = os.path.join('artifacts',"test.csv")
    raw_data_path:str = os.path.join('artifacts',"data.csv")
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        lg.info("Entered the data ingestion method")
        try:
            df = pd.read_csv('Notebook/data/stud.csv')
            lg.info("Converted data into dataframe")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            lg.info("Train test split initialted")
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            lg.info("Ingestion is completed")
            
            return(
                self.ingestion_config.train_data_path,self.ingestion_config.test_data_path
            )
            
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    object = DataIngestion()
    train_data,test_data = object.initiate_data_ingestion()
    
    data_transformation = DataTransformation()
    train_arr,test_arr,_ = data_transformation.init_ate_data_transform(train_data,test_data)
    
    modelTrainer = ModelTrainer()
    print(modelTrainer.initiate_model_training(train_arr,test_arr))