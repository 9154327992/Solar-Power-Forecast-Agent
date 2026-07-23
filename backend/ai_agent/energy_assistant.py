# ============================================================
# energy_assistant.py
# AI Energy Assistant
# ============================================================

from datetime import datetime


class EnergyAssistant:

    def __init__(self):
        self.name = "Solar AI Assistant"

    # ========================================================
    # Answer User Question
    # ========================================================

    def chat(self, message: str):

        message = message.lower().strip()

        if "hello" in message or "hi" in message:
            return (
                "Hello! I'm your Solar Energy Assistant. "
                "How can I help you today?"
            )

        elif "solar" in message:
            return (
                "Solar panels generate more electricity when "
                "solar radiation is high and cloud cover is low."
            )

        elif "weather" in message:
            return (
                "Weather conditions such as sunshine, "
                "temperature, humidity and cloud cover directly "
                "affect solar power generation."
            )

        elif "battery" in message:
            return (
                "Store excess solar energy in batteries during "
                "peak generation for later use."
            )

        elif "forecast" in message:
            return (
                "The forecasting model predicts solar power "
                "generation using weather parameters."
            )

        elif "efficiency" in message:
            return (
                "Keep your solar panels clean and avoid shading "
                "to improve overall efficiency."
            )

        else:
            return (
                "I can answer questions about solar energy, "
                "weather, power forecasting, batteries, and "
                "energy optimization."
            )

    # ========================================================
    # Generate Prediction Insight
    # ========================================================

    def generate_insight(self, prediction):

        power = prediction["prediction"]
        level = prediction["level"]

        if level == "Excellent 🌞":

            return (
                f"Excellent conditions detected. Expected power "
                f"generation is {power:.2f} W. Consider exporting "
                "surplus electricity to the grid."
            )

        elif level == "High ☀":

            return (
                f"High solar generation expected ({power:.2f} W). "
                "Operate heavy appliances during daylight hours."
            )

        elif level == "Moderate ⛅":

            return (
                f"Moderate generation ({power:.2f} W). "
                "Manage energy usage efficiently."
            )

        else:

            return (
                f"Low solar generation ({power:.2f} W). "
                "Battery backup may be required."
            )

    # ========================================================
    # Daily Summary
    # ========================================================

    def daily_summary(self):

        today = datetime.now().strftime("%d %B %Y")

        return (
            f"Solar Energy Summary ({today})\n\n"
            "- Monitor today's weather.\n"
            "- Use appliances during peak sunlight.\n"
            "- Keep panels clean.\n"
            "- Store excess energy in batteries."
        )


# ============================================================
# Global Assistant Object
# ============================================================

assistant = EnergyAssistant()


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    print(assistant.chat("Hello"))

    sample_prediction = {

        "prediction": 5430.25,

        "level": "Excellent 🌞"

    }

    print()

    print(assistant.generate_insight(sample_prediction))

    print()

    print(assistant.daily_summary())