import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import Datatransformartion
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException


class TrainingPipeline:
    def start_data_ingestion(self):
        """
        Runs the data ingestion process and returns the path
        to the feature store file (CSV or similar).
        """
        try:
            data_ingestion = DataIngestion()
            feature_store_file_path = data_ingestion.Initiate_data_ingestion()
            return feature_store_file_path
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_transformation(self, feature_store_file_path):
        """
        Transforms the ingested data and returns transformed train/test arrays and the preprocessor.
        """
        try:
            data_transformation = Datatransformartion(
                feature_store_file_path=feature_store_file_path
            )
            train_arr, test_arr, preprocessor = data_transformation.initiate_data_transformation()
            return train_arr, test_arr, preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_training(self, train_arr, test_arr):
        """
        Trains the model and returns the evaluation score (e.g., R² score).
        """
        try:
            model_trainer = ModelTrainer()
            model_score = model_trainer.initiate_model_trainer(train_arr, test_arr)
            return model_score
        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self):
        """
        Executes the full ML training pipeline and returns the model's R² score.
        """
        try:
            feature_store_file_path = self.start_data_ingestion()
            train_arr, test_arr, preprocessor = self.start_data_transformation(feature_store_file_path)
            r2_score = self.start_model_training(train_arr, test_arr)

            print("✅ Training completed. R² score:", r2_score)
            return r2_score
        except Exception as e:
            raise CustomException(e, sys)
