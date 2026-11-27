
from fastapi import FastAPI
from app.routers import prediction

app = FastAPI(
    title="Uber Fare Prediction API",
    description="Machine Learning Based Uber Fare Prediction",
    version="1.0.0"
)

app.include_router(prediction.router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Uber Fare Prediction API",
        "status": "Running Successfully"
    }

@app.get("/health")
def health():
    return {"status": "Healthy"}

