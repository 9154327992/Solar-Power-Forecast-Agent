from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def weather_home():
    return {"message": "Weather API"}


@router.get("/current/{city}")
def current_weather(city: str):
    return {
        "city": city,
        "message": "Current weather endpoint"
    }


@router.get("/forecast/{city}")
def forecast(city: str):
    return {
        "city": city,
        "message": "Forecast endpoint"
    }