# ============================================================
# weather_explainer.py
# Weather Impact Explainer
# ============================================================

class WeatherExplainer:
    """
    Explains how weather conditions affect
    solar power generation.
    """

    def explain(self, weather_data):

        temperature = weather_data.get("temperature", 0)
        humidity = weather_data.get("humidity", 0)
        cloud_cover = weather_data.get("cloud_cover", 0)
        wind_speed = weather_data.get("wind_speed", 0)
        description = weather_data.get("description", "").capitalize()

        explanations = []

        # Sky Condition
        explanations.append(f"Current weather: {description}.")

        # Cloud Cover
        if cloud_cover <= 20:
            explanations.append(
                "Low cloud cover allows maximum sunlight to reach the solar panels."
            )
        elif cloud_cover <= 60:
            explanations.append(
                "Moderate cloud cover may slightly reduce solar energy production."
            )
        else:
            explanations.append(
                "Heavy cloud cover significantly reduces solar power generation."
            )

        # Temperature
        if 15 <= temperature <= 30:
            explanations.append(
                "The temperature is within the ideal operating range for solar panels."
            )
        elif temperature > 35:
            explanations.append(
                "High temperatures can slightly reduce panel efficiency."
            )
        else:
            explanations.append(
                "Cool temperatures generally do not negatively affect panel performance."
            )

        # Humidity
        if humidity > 80:
            explanations.append(
                "High humidity may reduce sunlight intensity reaching the panels."
            )

        # Wind
        if wind_speed > 8:
            explanations.append(
                "Moderate wind helps cool solar panels, improving efficiency."
            )

        return explanations

    def summary(self, weather_data):

        return {
            "weather": weather_data,
            "explanation": self.explain(weather_data)
        }


# Global instance
weather_explainer = WeatherExplainer()