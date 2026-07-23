# ============================================================
# weather_utils.py
# Weather Utility Functions
# ============================================================

from datetime import datetime


class WeatherUtils:
    """
    Utility functions for weather processing.
    """

    @staticmethod
    def estimate_sunshine(cloud_cover):
        """
        Estimate sunshine percentage from cloud cover.
        """

        return max(0, 100 - cloud_cover)

    @staticmethod
    def estimate_radiation(cloud_cover):
        """
        Estimate solar radiation (W/m²).
        """

        return round((100 - cloud_cover) * 10, 2)

    @staticmethod
    def celsius_to_fahrenheit(temp):
        """
        Convert Celsius to Fahrenheit.
        """

        return round((temp * 9 / 5) + 32, 2)

    @staticmethod
    def kmh_to_ms(speed):
        """
        Convert km/h to m/s.
        """

        return round(speed / 3.6, 2)

    @staticmethod
    def weather_score(cloud_cover, humidity):
        """
        Calculate a simple weather suitability score (0–100)
        for solar power generation.
        """

        score = 100

        score -= cloud_cover * 0.6
        score -= max(0, humidity - 50) * 0.3

        return max(0, round(score, 2))

    @staticmethod
    def is_good_weather(cloud_cover):
        """
        Check if weather is favorable for solar generation.
        """

        return cloud_cover < 40

    @staticmethod
    def current_timestamp():
        """
        Current date and time.
        """

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Global instance
weather_utils = WeatherUtils()