# ============================================================
# test_weather.py
# ============================================================

import unittest

from backend.weather.preprocessing import preprocess_weather


class TestWeather(unittest.TestCase):

    def test_weather_preprocessing(self):

        weather = {
            "city": "Kathmandu",
            "temperature": 28,
            "humidity": 55,
            "pressure": 1012,
            "wind_speed": 3.2,
            "cloud_cover": 20,
            "description": "clear sky"
        }

        features = preprocess_weather(weather)

        self.assertIsInstance(features, dict)

        expected_features = [
            "WindSpeed",
            "Sunshine",
            "AirPressure",
            "Radiation",
            "AirTemperature",
            "RelativeAirHumidity",
            "Hour",
            "Day",
            "Month"
        ]

        for feature in expected_features:
            self.assertIn(feature, features)

        self.assertGreaterEqual(features["Sunshine"], 0)
        self.assertGreaterEqual(features["Radiation"], 0)
        self.assertGreater(features["AirPressure"], 0)


if __name__ == "__main__":
    unittest.main()