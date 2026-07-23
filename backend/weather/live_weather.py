# ============================================================
# live_weather.py
# Live Weather Service
# ============================================================

from backend.weather.weather_api import get_current_weather
from backend.weather.preprocessing import preprocess_weather
from backend.weather.weather_utils import weather_utils


class LiveWeather:
    """
    Handles fetching and processing live weather data.
    """

    def get_weather(self, city):
        """
        Fetch current weather for a city.
        """

        return get_current_weather(city)

    def get_processed_weather(self, city):
        """
        Fetch and preprocess weather for prediction.
        """

        weather = self.get_weather(city)

        features = preprocess_weather(weather)

        return {
            "weather": weather,
            "features": features
        }

    def weather_summary(self, city):
        """
        Generate a weather summary.
        """

        weather = self.get_weather(city)

        score = weather_utils.weather_score(
            weather["cloud_cover"],
            weather["humidity"]
        )

        return {
            "city": weather["city"],
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "cloud_cover": weather["cloud_cover"],
            "wind_speed": weather["wind_speed"],
            "description": weather["description"],
            "weather_score": score,
            "good_for_solar": weather_utils.is_good_weather(
                weather["cloud_cover"]
            )
        }


# Global instance
live_weather = LiveWeather()