
from pydantic import BaseModel, Field

class FarePredictionRequest(BaseModel):
    distance_km: float = Field(gt=0, le=500)
    city: str
    hour: int = Field(ge=0, le=23)
    day_of_week: int = Field(ge=0, le=6)
    is_weekend: int = Field(ge=0, le=1)
    payment_method: str

class FarePredictionResponse(BaseModel):
    status: str
    predicted_fare: float
    message: str
