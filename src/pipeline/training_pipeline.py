import sys 
import os

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import Datatransformartion
from src.components.model_trainer import ModelTrainer

from src.exception import Custom_exception


class TrainingPipeline:

    def start_data_ingestion(self):

        try:
            data_ingestion = DataIngestion()
            feature_store_file_path = data_ingestion.Initiate_data_ingestion()

            return feature_store_file_path
        
        except Exception as e:
            raise Custom_exception(e,sys)
        
    def start_data_transformation(self,feature_store_file_path):

        try:
            data_transformation = Datatransformartion(feature_store_file_path= feature_store_file_path)
            train_arr, test_arr ,preprocessor = data_transformation.initiate_data_transformation()

            return train_arr , test_arr , preprocessor
        
        except Exception as e:
            raise Custom_exception(e , sys)
        

    def start_model_training(self,train_arr , test_arr):

        try:
            Model_Trainer = ModelTrainer()
            model_score = Model_Trainer.initiate_model_trainer(
                train_arr , test_arr
            )

            return model_score
        except Exception as e:
            raise Custom_exception(e,sys)
        
    def run_pipeline(self):
        try:
            feature_store_file_path = self.start_data_ingestion()
            train_arr , test_arr , preprocessor = self.start_data_transformation(feature_store_file_path)
            r2_square = self.start_model_training(train_arr , test_arr)

            print("Training completed. trained model score:", r2_square)

        except Exception as e:
            raise Custom_exception(e, sys)
        
        