# ============================================================
# helper.py
# Utility Functions
# ============================================================

import os
from datetime import datetime
import json

# ============================================================
# Current Timestamp
# ============================================================

def current_timestamp():
    """
    Return current date and time.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================================
# Ensure Directory Exists
# ============================================================

def create_directory(directory):

    """
    Create directory if it does not exist.
    """

    os.makedirs(directory, exist_ok=True)


# ============================================================
# Save JSON File
# ============================================================

def save_json(data, filepath):

    """
    Save dictionary to JSON file.
    """

    create_directory(os.path.dirname(filepath) or ".")

    with open(filepath, "w", encoding="utf-8") as file:

        json.dump(data, file, indent=4)


# ============================================================
# Load JSON File
# ============================================================

def load_json(filepath):

    """
    Load JSON file.
    """

    with open(filepath, "r", encoding="utf-8") as file:

        return json.load(file)


# ============================================================
# Round Float Values
# ============================================================

def round_value(value, digits=2):

    """
    Round float value.
    """

    return round(float(value), digits)


# ============================================================
# Prediction Level
# ============================================================

def prediction_level(power):

    """
    Determine solar generation level.
    """

    if power >= 5000:
        return "Excellent 🌞"

    elif power >= 2000:
        return "High ☀"

    elif power >= 500:
        return "Moderate ⛅"

    return "Low 🌙"


# ============================================================
# Efficiency Calculator
# ============================================================

def calculate_efficiency(power, maximum_power=7701):

    """
    Calculate efficiency percentage.
    """

    efficiency = (power / maximum_power) * 100

    efficiency = max(0, min(efficiency, 100))

    return round(efficiency, 2)


# ============================================================
# Format Power
# ============================================================

def format_power(power):

    """
    Format power output.
    """

    return f"{power:.2f} W"


# ============================================================
# Format Percentage
# ============================================================

def format_percentage(value):

    """
    Format percentage.
    """

    return f"{value:.2f}%"


# ============================================================
# Success Response
# ============================================================

def success_response(message, data=None):

    """
    Standard success response.
    """

    return {

        "success": True,

        "message": message,

        "data": data

    }


# ============================================================
# Error Response
# ============================================================

def error_response(message):

    """
    Standard error response.
    """

    return {

        "success": False,

        "message": message

    }


# ============================================================
# Test Module
# ============================================================

if __name__ == "__main__":

    print(current_timestamp())

    print(prediction_level(5300))

    print(calculate_efficiency(5300))

    print(format_power(5300))

    print(format_percentage(91.42))

    print(success_response("Prediction completed"))

    print(error_response("Invalid weather data"))