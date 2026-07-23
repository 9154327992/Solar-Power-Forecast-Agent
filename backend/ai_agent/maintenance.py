# ============================================================
# maintenance.py
# Solar Panel Maintenance Advisor
# ============================================================

from datetime import datetime


class MaintenanceAdvisor:
    """
    Provides maintenance recommendations based on
    predicted solar power generation.
    """

    def __init__(self):
        self.max_power = 7701  # Maximum system production (W)

    def performance_level(self, prediction):
        """Determine system performance level."""

        percentage = (prediction / self.max_power) * 100

        if percentage >= 80:
            return "Excellent"

        elif percentage >= 60:
            return "Good"

        elif percentage >= 40:
            return "Average"

        elif percentage >= 20:
            return "Poor"

        return "Critical"

    def recommendations(self, prediction):

        level = self.performance_level(prediction)

        if level == "Excellent":
            return [
                "Solar panels are operating efficiently.",
                "Continue regular monthly inspections.",
                "No maintenance required at this time."
            ]

        elif level == "Good":
            return [
                "Inspect panels for dust accumulation.",
                "Check inverter status.",
                "Monitor energy production."
            ]

        elif level == "Average":
            return [
                "Clean the solar panels.",
                "Inspect for shading from nearby trees or buildings.",
                "Verify wiring and inverter connections."
            ]

        elif level == "Poor":
            return [
                "Perform a complete panel cleaning.",
                "Inspect for damaged panels or loose cables.",
                "Schedule a professional system inspection."
            ]

        return [
            "Immediate maintenance recommended.",
            "Inspect inverter and battery system.",
            "Contact a certified solar technician."
        ]

    def next_service(self):
        """Suggested maintenance interval."""

        return "Every 6 months"

    def generate(self, prediction):
        """Generate complete maintenance report."""

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": round(prediction, 2),
            "performance": self.performance_level(prediction),
            "next_service": self.next_service(),
            "recommendations": self.recommendations(prediction)
        }


# Global instance
maintenance = MaintenanceAdvisor()