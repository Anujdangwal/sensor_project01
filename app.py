from flask import Flask, render_template, request, send_file
from src.exception import CustomException
from src.logger import logging as lg
import os
import sys

from src.pipeline.training_pipeline import TrainingPipeline
from src.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/train")
def train_route():
    try:
        train_pipeline = TrainingPipeline()
        accuracy = train_pipeline.run_pipeline()  # returns float

        return f"""
        <html>
        <head><title>Training Complete</title></head>
        <body style='text-align:center; padding-top:50px; font-family:Arial; background-color:#f4f4f4;'>
            <h1 style='color:#2c3e50;'>✅ Model Training Completed</h1>
            <h2 style='color:#27ae60;'>📊 Accuracy (R² Score): {accuracy:.4f}</h2>
            <br>
            <a href="/" style="font-size:18px; text-decoration:none; color:#2980b9;">⬅️ Back to Home</a>
        </body>
        </html>
        """

    except Exception as e:
        raise CustomException(e, sys)

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    try:
        if request.method == 'POST':
            prediction_pipeline = PredictionPipeline(request)
            prediction_file_path = prediction_pipeline.run_pipeline()

            lg.info("Prediction completed. Downloading prediction file.")
            return send_file(
                prediction_file_path,
                download_name=os.path.basename(prediction_file_path),
                as_attachment=True
            )
        else:
            return render_template('upload_file.html')

    except Exception as e:
        raise CustomException(e, sys)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
