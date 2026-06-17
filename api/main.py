from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(
    title="Parkinson's Disease Detection API"
)

model = joblib.load(
    "models/xgboost_model.pkl"
)

class ParkinsonInput(BaseModel):
    features: list[float]

@app.get("/")
def home():
    return {
        "message": "Parkinson's Detection API is running"
    }

@app.post("/predict")
def predict(data: ParkinsonInput):

    prediction = model.predict(
        np.array([data.features])
    )[0]

    return {
        "prediction": int(prediction)
    }