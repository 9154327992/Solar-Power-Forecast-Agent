# ============================================================
# weather_service.py
# Weather Service
# ============================================================

from backend.weather.weather_api import get_current_weather
from backend.weather.preprocessing import preprocess_weather
from backend.weather.weather_utils import weather_utils


class WeatherService:
    """
    Service for fetching and processing weather data.
    """

    def get_live_weather(self, city):
        """
        Fetch current weather data.
        """
        return get_current_weather(city)

    def get_prediction_features(self, city):
        """
        Fetch weather and convert it to ML model features.
        """
        weather = self.get_live_weather(city)

        features = preprocess_weather(weather)

        return features

    def get_weather_report(self, city):
        """
        Generate a weather report for the UI.
        """
        weather = self.get_live_weather(city)

        score = weather_utils.weather_score(
            weather["cloud_cover"],
            weather["humidity"]
        )

        report = {
            "city": weather["city"],
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "pressure": weather["pressure"],
            "wind_speed": weather["wind_speed"],
            "cloud_cover": weather["cloud_cover"],
            "description": weather["description"],
            "weather_score": score,
            "solar_friendly": weather_utils.is_good_weather(
                weather["cloud_cover"]
            )
        }

        return report

    def get_complete_weather_data(self, city):
        """
        Return both raw weather and processed features.
        """
        weather = self.get_live_weather(city)

        features = preprocess_weather(weather)

        return {
            "weather": weather,
            "features": features
        }


# Global instance
weather_service = WeatherService()