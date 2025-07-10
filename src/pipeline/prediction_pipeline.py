import os
import sys
import pandas as pd
from flask import request
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException
from src.constant import *
from src.utils.main_utils import MainUtils


@dataclass
class PredictionPipelineConfig:
    prediction_output_dirname: str = "predictions"
    prediction_file_name: str = "prediction_file.csv"
    model_file_path: str = os.path.join(artifact_folder, "model.pkl")
    preprocessor_path: str = os.path.join(artifact_folder, "preprocessor.pkl")
    prediction_file_path: str = os.path.join(prediction_output_dirname, prediction_file_name)


class PredictionPipeline:
    def __init__(self, request: request):
        self.request = request
        self.utils = MainUtils()
        self.prediction_pipeline_config = PredictionPipelineConfig()

    def save_input_file(self) -> str:
        """
        Save uploaded file from HTML form to local directory.
        """
        try:
            pred_file_input_dir = "prediction_artifacts"
            os.makedirs(pred_file_input_dir, exist_ok=True)

            input_csv_file = self.request.files["file"]

            # Ensure it's a CSV
            if not input_csv_file.filename.endswith(".csv"):
                raise CustomException("Uploaded file is not a CSV", sys)

            pred_file_path = os.path.join(pred_file_input_dir, input_csv_file.filename)
            input_csv_file.save(pred_file_path)

            logging.info(f"File saved at: {pred_file_path}")
            return pred_file_path

        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, features: pd.DataFrame):
        """
        Load model and preprocessor, perform prediction.
        """
        try:
            model = self.utils.load_object(self.prediction_pipeline_config.model_file_path)
            preprocessor = self.utils.load_object(self.prediction_pipeline_config.preprocessor_path)

            transformed_x = preprocessor.transform(features)
            preds = model.predict(transformed_x)

            return preds

        except Exception as e:
            raise CustomException(e, sys)

    def get_prediction_dataframe(self, input_dataframe_path: str) -> str:
        """
        Load input CSV, predict, save and return prediction path.
        """
        try:
            prediction_column_name: str = TARGET_COLUMN

            input_dataframe: pd.DataFrame = pd.read_csv(input_dataframe_path)

            # Drop unnamed index column if present
            if "unnamed: 0" in input_dataframe.columns or "Unnamed: 0" in input_dataframe.columns:
                input_dataframe.drop(columns=["unnamed: 0", "Unnamed: 0"], inplace=True, errors='ignore')

            # Run prediction
            predictions = self.predict(input_dataframe)

            input_dataframe[prediction_column_name] = [int(pred) for pred in predictions]
            input_dataframe[prediction_column_name] = input_dataframe[prediction_column_name].map({0: "bad", 1: "good"})

            os.makedirs(self.prediction_pipeline_config.prediction_output_dirname, exist_ok=True)

            input_dataframe.to_csv(self.prediction_pipeline_config.prediction_file_path, index=False)

            logging.info(f"Prediction saved to: {self.prediction_pipeline_config.prediction_file_path}")

            return self.prediction_pipeline_config.prediction_file_path

        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self) -> str:
        """
        Main method to orchestrate the prediction pipeline.
        """
        try:
            input_csv_path = self.save_input_file()
            prediction_path = self.get_prediction_dataframe(input_csv_path)
            return prediction_path

        except Exception as e:
            raise CustomException(e, sys)
