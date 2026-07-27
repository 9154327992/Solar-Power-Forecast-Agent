from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class RecommendationRequest(BaseModel):
    predicted_power: float
    battery_level: float
    weather: str


@router.get("/")
def recommendation_home():
    return {
        "message": "Energy Recommendation API"
    }


@router.post("/")
def energy_recommendation(request: RecommendationRequest):

    recommendations = []

    if request.predicted_power >= 6:
        recommendations.append(
            "High solar generation expected. Run high-power appliances during daylight hours."
        )
    elif request.predicted_power >= 3:
        recommendations.append(
            "Moderate solar generation expected. Balance solar usage with battery storage."
        )
    else:
        recommendations.append(
            "Low solar generation expected. Reduce non-essential electricity usage."
        )

    if request.battery_level < 30:
        recommendations.append(
            "Battery level is low. Charge when solar production increases."
        )

    if request.weather.lower() in ["rain", "cloudy", "storm"]:
        recommendations.append(
            "Cloudy or rainy conditions may reduce solar output."
        )

    return {
        "predicted_power": request.predicted_power,
        "battery_level": request.battery_level,
        "weather": request.weather,
        "recommendations": recommendations
    }


@router.get("/{city}")
def recommendation(city: str):

    return {
        "city": city,
        "recommendation": "Use solar energy during peak sunlight hours."
    }
