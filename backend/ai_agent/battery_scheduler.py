# ============================================================
# battery_scheduler.py
# Battery Charging & Usage Scheduler
# ============================================================

from datetime import datetime


class BatteryScheduler:
    """
    Generates battery charging and discharging recommendations
    based on predicted solar power generation.
    """

    def __init__(self):
        self.max_power = 7701  # Maximum system production (W)

    def battery_level(self, prediction):
        """Estimate solar generation level."""

        percentage = (prediction / self.max_power) * 100

        if percentage >= 80:
            return "Very High"

        elif percentage >= 60:
            return "High"

        elif percentage >= 40:
            return "Moderate"

        elif percentage >= 20:
            return "Low"

        return "Very Low"

    def schedule(self, prediction):
        """
        Generate battery charging schedule.
        """

        level = self.battery_level(prediction)

        if level == "Very High":
            return {
                "status": level,
                "charge": "Charge battery to 100%.",
                "usage": "Run high-power appliances during daylight.",
                "grid": "Minimal grid usage expected."
            }

        elif level == "High":
            return {
                "status": level,
                "charge": "Charge battery normally.",
                "usage": "Use solar energy for most household loads.",
                "grid": "Low dependence on the grid."
            }

        elif level == "Moderate":
            return {
                "status": level,
                "charge": "Charge battery if below 50%.",
                "usage": "Use battery during evening peak hours.",
                "grid": "Moderate grid support may be required."
            }

        elif level == "Low":
            return {
                "status": level,
                "charge": "Conserve battery charge.",
                "usage": "Reduce non-essential electricity consumption.",
                "grid": "Grid power likely required."
            }

        return {
            "status": level,
            "charge": "Do not rely on solar charging today.",
            "usage": "Reserve battery for emergency or night use.",
            "grid": "High grid dependence expected."
        }

    def best_charging_time(self):
        """
        Suggest the ideal charging window.
        """

        return "10:00 AM - 2:00 PM"

    def generate(self, prediction):
        """
        Complete battery scheduling recommendation.
        """

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": round(prediction, 2),
            "best_charging_time": self.best_charging_time(),
            "recommendation": self.schedule(prediction)
        }


# Global instance
battery_scheduler = BatteryScheduler()