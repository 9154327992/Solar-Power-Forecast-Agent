# ============================================================
# weather_api.py
# OpenWeatherMap Weather API
# ============================================================

import os
import requests

from dotenv import load_dotenv

# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# ============================================================
# Get Weather by City
# ============================================================

def get_current_weather(city):

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    response.raise_for_status()

    data = response.json()

    weather = {

        "city": data["name"],

        "temperature": data["main"]["temp"],

        "humidity": data["main"]["humidity"],

        "pressure": data["main"]["pressure"],

        "wind_speed": data["wind"]["speed"],

        "cloud_cover": data["clouds"]["all"],

        "description": data["weather"][0]["description"]

    }

    return weather


# ============================================================
# Get Weather by Coordinates
# ============================================================

def get_weather_by_coordinates(latitude, longitude):

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    response.raise_for_status()

    data = response.json()

    weather = {

        "city": data["name"],

        "temperature": data["main"]["temp"],

        "humidity": data["main"]["humidity"],

        "pressure": data["main"]["pressure"],

        "wind_speed": data["wind"]["speed"],

        "cloud_cover": data["clouds"]["all"],

        "description": data["weather"][0]["description"]

    }

    return weather


# ============================================================
# API Status Check
# ============================================================

def check_api_connection():

    try:

        get_current_weather("London")

        return True

    except Exception:

        return False


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    print(get_current_weather("New York"))