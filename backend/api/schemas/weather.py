"""
Weather Schemas
"""

from pydantic import BaseModel


class WeatherRequest(BaseModel):
    city: str


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    radiation: float
    sunshine: float


class ForecastResponse(BaseModel):
    city: str
    forecast: list