from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: float
    wind_speed: float
    condition: str


@router.get("/")
def weather_home():
    return {
        "message": "Weather API is running"
    }


@router.get("/current/{city}")
def current_weather(city: str):

    # Replace these values with data from OpenWeatherMap or another weather API.
    return {
        "city": city,
        "temperature": 31.5,
        "humidity": 68,
        "wind_speed": 12.4,
        "condition": "Sunny"
    }


@router.get("/forecast/{city}")
def forecast(city: str):

    # Example 3-day forecast
    return {
        "city": city,
        "forecast": [
            {
                "day": "Today",
                "temperature": 31,
                "condition": "Sunny"
            },
            {
                "day": "Tomorrow",
                "temperature": 29,
                "condition": "Partly Cloudy"
            },
            {
                "day": "Day 3",
                "temperature": 28,
                "condition": "Cloudy"
            }
        ]
    }
