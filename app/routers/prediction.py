from fastapi import APIRouter

from app.schemas import (
    FarePredictionRequest,
    FarePredictionResponse
)

from app.services.prediction_service import predict_fare


router = APIRouter(
    prefix="/prediction",
    tags=["Fare Prediction"]
)


@router.post(
    "/predict",
    response_model=FarePredictionResponse
)
def predict(request: FarePredictionRequest):

    predicted_fare = predict_fare(request)

    return {
        "status": "success",
        "predicted_fare": predicted_fare,
        "message": "Uber fare predicted successfully"
    }