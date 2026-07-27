from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class MaintenanceRequest(BaseModel):
    panel_efficiency: float
    dust_level: float
    battery_health: float


@router.get("/")
def maintenance_home():
    return {
        "message": "Solar Maintenance API"
    }


@router.post("/advice")
def maintenance_advice(request: MaintenanceRequest):

    advice = []

    if request.panel_efficiency < 80:
        advice.append("Clean solar panels.")

    if request.dust_level > 60:
        advice.append("High dust detected. Schedule panel cleaning.")

    if request.battery_health < 70:
        advice.append("Battery health is low. Inspect or replace the battery.")

    if not advice:
        advice.append("System is operating normally. No maintenance required.")

    return {
        "panel_efficiency": request.panel_efficiency,
        "dust_level": request.dust_level,
        "battery_health": request.battery_health,
        "maintenance_recommendations": advice
    }


@router.get("/{city}")
def maintenance(city: str):

    return {
        "city": city,
        "maintenance": "No maintenance required.",
        "next_service": "30 days"
    }
