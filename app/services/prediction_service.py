
import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "fare_model.pkl"

model = joblib.load(MODEL_PATH)

def predict_fare(data):

    input_data = pd.DataFrame([{
        "distance_km": data.distance_km,
        "city": data.city,
        "hour": data.hour,
        "day_of_week": data.day_of_week,
        "is_weekend": data.is_weekend,
        "payment_method": data.payment_method
    }])

    prediction = model.predict(input_data)

    return round(float(prediction[0]), 2)
