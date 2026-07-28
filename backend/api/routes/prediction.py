from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

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


class PredictionResponse(BaseModel):
    prediction: float
    level: str
    efficiency: float
    recommendation: str


@router.get("/")
def prediction_home():
    return {"message": "Prediction API is running"}


@router.post("/forecast", response_model=PredictionResponse)
def forecast(request: PredictionRequest):
    try:
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

        history = {
            "predicted_power": prediction,
            "generation_level": level,
            "efficiency": efficiency
        }

        try:
            requests.post(
                "http://127.0.0.1:8000/api/history",
                json=history,
                timeout=2
            )
        except Exception:
            pass

        prediction_history.append({
            "predicted_power": prediction,
            "generation_level": level,
            "efficiency": efficiency,
            "recommendation": "Good conditions for solar generation."
        })
        return PredictionResponse(
            prediction=prediction,
            level=level,
            efficiency=efficiency,
            recommendation="Good conditions for solar generation."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
