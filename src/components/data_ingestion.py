import sys
import os

import numpy as np
import pandas as pd

import pymongo
from pymongo import MongoClient
from zipfile import Path
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    artifact_folder:str = os.path.join(artifact_folder)


class DataIngestion:
    def __init__(self):
        self.Data_Ingestion_Config = DataIngestionConfig()
        self.utils = MainUtils()

    def Export_collection_as_DataFrame(self, collection_name , db_name):

        try:
            client = MongoClient(MONGO_DB_URL)
            
            collection = client[MONGO_DATABASE_NAME][MONGO_COLLECTION_NAME]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.tolist():
                df = df.drop(columns= ["_id"] , axis = 1)

            df.replace({"na" : np.nan}, inplace=True)

            return df
        
        except Exception as e:
            raise CustomException(e , sys)
        

        
    def Export_data_into_Feature_store_file_path(self)-> pd.DataFrame:

        try:

            logging.info(f"exporting our Data from mongodb")
            raw_file_path = self.Data_Ingestion_Config.artifact_folder

            os.makedirs(raw_file_path, exist_ok= True)


            sensor_data = self.Export_collection_as_DataFrame(
                collection_name= MONGO_COLLECTION_NAME,
                db_name= MONGO_DATABASE_NAME
            )

            logging.info(f"Saving Exported data into feature store file path : {raw_file_path}")

            Feature_store_file_path = os.path.join(raw_file_path , "wafer_fault.csv")

            sensor_data.to_csv(Feature_store_file_path , index = False)

            return Feature_store_file_path
        
        except Exception as e:
            raise CustomException(e ,sys)


    def Initiate_data_ingestion(self)-> Path:

        logging.info("Entered Initiated_data_ingestion method of data_ingestion class")

        try:
            feature_store_file_path = self.Export_data_into_Feature_store_file_path()

            logging.info("got the data from mongodb")
        
            logging.info("Exited initiate_data_ingestion methods of data ingestion class")

            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e, sys) from e
