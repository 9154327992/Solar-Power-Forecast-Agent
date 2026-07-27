from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class BatteryRequest(BaseModel):
    battery_level: float
    predicted_power: float


@router.get("/")
def battery_home():
    return {
        "message": "Battery Scheduling API"
    }


@router.post("/schedule")
def battery_schedule(request: BatteryRequest):

    if request.predicted_power >= 5:
        action = "Charge Battery"
    elif request.battery_level >= 80:
        action = "Use Stored Energy"
    else:
        action = "Normal Operation"

    return {
        "battery_level": request.battery_level,
        "predicted_power": request.predicted_power,
        "recommended_action": action
    }


@router.get("/{city}")
def battery(city: str):

    return {
        "city": city,
        "recommended_action": "Normal Operation",
        "message": "Battery scheduling information."
    }
