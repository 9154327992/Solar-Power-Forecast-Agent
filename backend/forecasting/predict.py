# ============================================================
# predict.py
# Solar Power Prediction
# ============================================================

import pandas as pd

from backend.forecasting.model_loader import model_loader
from backend.utils.constants import MAX_SOLAR_POWER


class SolarPredictor:
    """
    Performs solar power prediction using the trained model.
    """

    def __init__(self):
        self.model, self.scaler = model_loader.load()

    def prediction_level(self, value):

        if value < MAX_SOLAR_POWER * 0.30:
            return "Low"

        elif value < MAX_SOLAR_POWER * 0.70:
            return "Moderate"

        return "High"

    def efficiency(self, value):

        return round((value / MAX_SOLAR_POWER) * 100, 2)

    def recommendation(self, level):

        recommendations = {
            "Low": "Reduce electricity consumption and rely on the grid if necessary.",
            "Moderate": "Normal solar production expected. Schedule medium-load appliances.",
            "High": "Excellent solar production. Ideal time to run heavy electrical appliances or charge batteries."
        }

        return recommendations[level]

    def predict(self, features):
        """
        Predict solar power.

        Parameters
        ----------
        features : dict
            {
                WindSpeed,
                Sunshine,
                AirPressure,
                Radiation,
                AirTemperature,
                RelativeAirHumidity,
                Hour,
                Day,
                Month
            }
        """

        feature_order = [
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

        df = pd.DataFrame([features])[feature_order]

        scaled = self.scaler.transform(df)

        prediction = float(self.model.predict(scaled)[0])

        prediction = max(0, round(prediction, 2))

        level = self.prediction_level(prediction)

        return {
            "prediction": prediction,
            "level": level,
            "efficiency": self.efficiency(prediction),
            "recommendation": self.recommendation(level)
        }


# Global instance
predictor = SolarPredictor()