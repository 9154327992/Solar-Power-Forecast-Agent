# ============================================================
# recommendation.py
# Solar Energy Recommendation Engine
# ============================================================

class RecommendationEngine:

    def __init__(self):
        pass

    # ========================================================
    # Generation Level
    # ========================================================

    def generation_level(self, power):

        if power >= 5000:
            return "Excellent 🌞"

        elif power >= 2000:
            return "High ☀"

        elif power >= 500:
            return "Moderate ⛅"

        else:
            return "Low 🌙"

    # ========================================================
    # Power Recommendation
    # ========================================================

    def power_recommendation(self, power):

        level = self.generation_level(power)

        recommendations = {

            "Excellent 🌞":
            [
                "Charge battery storage.",
                "Export surplus electricity to the grid.",
                "Run heavy electrical appliances.",
                "Excellent day for maximum solar production."
            ],

            "High ☀":
            [
                "Use washing machine or dishwasher now.",
                "Charge electric vehicles.",
                "Good opportunity to store energy."
            ],

            "Moderate ⛅":
            [
                "Operate essential appliances only.",
                "Monitor battery charge level.",
                "Reduce unnecessary energy consumption."
            ],

            "Low 🌙":
            [
                "Use battery backup if available.",
                "Reduce electricity usage.",
                "Avoid operating heavy appliances."
            ]

        }

        return {

            "level": level,

            "recommendations": recommendations[level]

        }

    # ========================================================
    # Weather Recommendation
    # ========================================================

    def weather_recommendation(self, weather):

        advice = []

        if weather["cloud_cover"] > 70:
            advice.append(
                "Heavy cloud cover may reduce solar output."
            )

        if weather["temperature"] > 35:
            advice.append(
                "High temperatures may slightly reduce panel efficiency."
            )

        if weather["wind_speed"] > 8:
            advice.append(
                "Strong winds can help cool solar panels."
            )

        if weather["humidity"] > 80:
            advice.append(
                "High humidity may reduce solar irradiance."
            )

        if len(advice) == 0:

            advice.append(
                "Weather conditions are favorable for solar generation."
            )

        return advice

    # ========================================================
    # Complete Recommendation
    # ========================================================

    def generate(self, prediction, weather):

        result = self.power_recommendation(prediction)

        weather_advice = self.weather_recommendation(weather)

        return {

            "prediction": prediction,

            "level": result["level"],

            "energy_recommendations": result["recommendations"],

            "weather_recommendations": weather_advice

        }


# ============================================================
# Global Object
# ============================================================

engine = RecommendationEngine()


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    prediction = 5400

    weather = {

        "temperature": 33,

        "humidity": 58,

        "wind_speed": 4,

        "cloud_cover": 20

    }

    recommendations = engine.generate(

        prediction,

        weather

    )

    print(recommendations)