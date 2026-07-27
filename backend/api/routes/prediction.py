from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class PredictionRequest(BaseModel):
    wind_speed: float
    sunshine_duration: float
    air_pressure: float
    solar_radiation: float
    air_temperature: float
    relative_humidity: float
    hour: int
    day: int
    month: int


@router.get("/")
def prediction_home():
    return {
        "message": "Prediction API is running"
    }


@router.post("/forecast")
def forecast(request: PredictionRequest):

    # Replace this with your trained ML model
    prediction = round(
        request.solar_radiation * 0.015 +
        request.sunshine_duration * 0.02,
        2
    )

    if prediction >= 6:
        level = "High"
    elif prediction >= 3:
        level = "Medium"
    else:
        level = "Low"

    efficiency = round(min(prediction * 15, 100), 2)

    return {
        "prediction": prediction,
        "level": level,
        "efficiency": efficiency,
        "recommendation": "Good conditions for solar generation."
    }
