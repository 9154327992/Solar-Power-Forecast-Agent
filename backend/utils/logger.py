# ============================================================
# logger.py
# Project Logger
# ============================================================

import logging
from pathlib import Path

# ------------------------------------------------------------
# Create logs directory
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "solar_forecast.log"

# ------------------------------------------------------------
# Configure Logger
# ------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("SolarForecast")