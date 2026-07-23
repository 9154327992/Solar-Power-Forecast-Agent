# ============================================================
# constants.py
# Project Constants
# ============================================================

# -------------------------------
# Application
# -------------------------------

APP_NAME = "Solar Power Forecast Agent"
APP_VERSION = "1.0.0"

# -------------------------------
# Model Information
# -------------------------------

MODEL_NAME = "XGBoost Regressor"

MAX_SOLAR_POWER = 7701

# -------------------------------
# Prediction Levels
# -------------------------------

LOW = "Low"
MODERATE = "Moderate"
HIGH = "High"

# -------------------------------
# Weather Thresholds
# -------------------------------

GOOD_CLOUD_COVER = 40
GOOD_HUMIDITY = 60
GOOD_TEMPERATURE_MIN = 20
GOOD_TEMPERATURE_MAX = 35

# -------------------------------
# Recommendation Messages
# -------------------------------

LOW_MESSAGE = (
    "Low solar generation expected. "
    "Consider reducing electricity usage."
)

MODERATE_MESSAGE = (
    "Moderate solar generation expected."
)

HIGH_MESSAGE = (
    "Excellent solar generation expected."
)

# -------------------------------
# Database
# -------------------------------

DATABASE_NAME = "solar_forecast.db"

# -------------------------------
# Reports
# -------------------------------

REPORT_FORMAT = "json"

# -------------------------------
# Date Format
# -------------------------------

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# -------------------------------
# Model Features
# -------------------------------

MODEL_FEATURES = [
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