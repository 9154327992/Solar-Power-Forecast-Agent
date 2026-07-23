# ============================================================
# config.py
# Project Configuration
# ============================================================

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ------------------------------------------------------------
# Base Directory
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ------------------------------------------------------------
# Dataset
# ------------------------------------------------------------

DATASET_PATH = BASE_DIR / "datasets" / "solar_power.csv"

# ------------------------------------------------------------
# Model Files
# ------------------------------------------------------------

MODEL_PATH = BASE_DIR / "models" / "model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

# ------------------------------------------------------------
# Database
# ------------------------------------------------------------

DATABASE_PATH = BASE_DIR / "solar_forecast.db"

# ------------------------------------------------------------
# Reports
# ------------------------------------------------------------

REPORTS_PATH = BASE_DIR / "reports"

# ------------------------------------------------------------
# API Keys
# ------------------------------------------------------------

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ------------------------------------------------------------
# Model Features
# ------------------------------------------------------------

MODEL_FEATURES = [
    "WindSpeed",
    "Sunshine",
    "AirPressure",
    "Radiation",
    "AirTemperature",
    "RelativeAirHumidity",
    "Hour",
    "Day",
    "Month",
]