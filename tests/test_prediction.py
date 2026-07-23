# ============================================================
# test_prediction.py
# ============================================================

import unittest

from backend.forecasting.predictor import predictor


class TestPrediction(unittest.TestCase):

    def test_prediction(self):

        sample = {
            "WindSpeed": 2.5,
            "Sunshine": 85,
            "AirPressure": 1013,
            "Radiation": 800,
            "AirTemperature": 28,
            "RelativeAirHumidity": 45,
            "Hour": 12,
            "Day": 15,
            "Month": 7
        }

        result = predictor.predict(sample)

        self.assertIsInstance(result, dict)

        self.assertIn("prediction", result)
        self.assertIn("level", result)
        self.assertIn("efficiency", result)
        self.assertIn("recommendation", result)

        self.assertGreaterEqual(result["prediction"], 0)


if __name__ == "__main__":
    unittest.main()