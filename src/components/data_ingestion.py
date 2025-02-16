import os
import sys


from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifacts
from src.exception import MyException
from src.logger import logging
from src.data_access.proj1_data import Proj1Data

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig = DataIngestionConfig()):
        try:
            logging.info("giving config to DataIngestion Class")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e,sys)
        
    def export_data_into_feature_store(self) -> DataFrame:
        try:
            logging.info(f"Exporting data from mongodb")
            my_data = Proj1Data()
            dataframe = my_data.export_collection_as_dataframe(collection_name= self.data_ingestion_config.collection_name)
            logging.info(f"Shape of Datafame : {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path  = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False , header=True)
            return dataframe
        except Exception as e:
            raise MyException(e,sys)
            
        
    def split_data_as_train_test(self,data_frame : DataFrame) ->None:
        logging.info("Entered into train test Split  of data Ingestion")
        try:
            train_set, test_set = train_test_split(data_frame,test_size= self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the given dataset")
            logging.info(
                            "Exited split_data_as_train_test method of Data_Ingestion class"
                        )
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header =True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index = False, header = True)
            
            logging.info(f"Exported train and test file path")
        except Exception as e:
            raise MyException(e, sys) from e
    
    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered into Data Ingestion Module")
        try:
            dataframe = self.export_data_into_feature_store()
            logging.info("Got tne data from mongo dn")
            
            self.split_data_as_train_test(data_frame= dataframe)
            
            logging.info("Performed train test split")
            logging.info(
                            "Exited initiate_data_ingestion method of Data_Ingestion class"
                        )
            
            
            data_ingestion_artifact = DataIngestionArtifacts(trained_file_path= self.data_ingestion_config.training_file_path,
                                                             test_file_path= self.data_ingestion_config.testing_file_path)
            
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys) from e