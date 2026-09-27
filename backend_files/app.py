
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import io

superkart_api = Flask(__name__)

# Load the serialized model
model = joblib.load("superkart_model.joblib")

@superkart_api.route("/")
def home():
    return "SuperKart Sales Prediction API is running!"

@superkart_api.post("/v1/predict")
def predict():
    """Online inference - single prediction"""
    data = request.get_json()
    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)
    return jsonify({"prediction": round(float(prediction[0]), 2)})

@superkart_api.post("/v1/predictbatch")
def predict_batch():
    """Batch inference - multiple predictions"""
    file = request.files["file"]
    input_df = pd.read_csv(io.StringIO(file.read().decode("utf-8")))
    predictions = model.predict(input_df)
    result = {str(i): round(float(pred), 2) for i, pred in enumerate(predictions)}
    return jsonify(result)

if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860)
