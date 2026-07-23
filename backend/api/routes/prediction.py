from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class PredictionRequest(BaseModel):
    city: str


@router.get("/")
def prediction_home():
    return {"message": "Prediction API"}


@router.post("/")
def predict(request: PredictionRequest):

    return {
        "city": request.city,
        "prediction": 0,
        "level": "Unknown",
        "efficiency": 0,
        "recommendation": "Prediction module not connected."
    }