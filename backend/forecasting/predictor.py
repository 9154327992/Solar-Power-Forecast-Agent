# ============================================================
# predictor.py
# Solar Power Prediction
# ============================================================

import os
import joblib
import pandas as pd


# ============================================================
# Paths
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")


# ============================================================
# Load Model
# ============================================================

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


# ============================================================
# Scale Features
# ============================================================

def scale_features(features: pd.DataFrame):

    return scaler.transform(features)


# ============================================================
# Generation Level
# ============================================================

def generation_level(power):

    if power >= 5000:
        return "Excellent"

    elif power >= 3000:
        return "High"

    elif power >= 1000:
        return "Moderate"

    return "Low"


# ============================================================
# Efficiency
# ============================================================

def calculate_efficiency(prediction, maximum_power=7701):

    efficiency = (prediction / maximum_power) * 100

    efficiency = max(0, min(efficiency, 100))

    return round(efficiency, 2)


# ============================================================
# Recommendation
# ============================================================

def recommendation(level):

    recommendations = {
        "Excellent": "Maximum solar generation expected. Operate high-power appliances during this period.",
        "High": "Good solar production. Ideal time for charging batteries and running household loads.",
        "Moderate": "Moderate production. Consider reducing non-essential loads.",
        "Low": "Low production expected. Use stored energy or grid power if necessary."
    }

    return recommendations[level]


# ============================================================
# AI Insight
# ============================================================

def insight(level):

    insights = {
        "Excellent": "Clear weather conditions are expected with excellent solar performance.",
        "High": "Favorable weather should support strong solar generation.",
        "Moderate": "Clouds or lower solar radiation may reduce production.",
        "Low": "Poor weather conditions are likely limiting solar output."
    }

    return insights[level]


# ============================================================
# Predict
# ============================================================

def predict(features: pd.DataFrame):

    scaled_features = scale_features(features)

    prediction = model.predict(scaled_features)[0]

    prediction = round(float(prediction), 2)

    level = generation_level(prediction)

    efficiency = calculate_efficiency(prediction)

    return {

        "prediction": prediction,

        "level": level,

        "efficiency": efficiency,

        "recommendation": recommendation(level),

        "insight": insight(level)

    }


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    sample = pd.DataFrame({

        "WindSpeed": [3.2],
        "Sunshine": [8.5],
        "AirPressure": [1012],
        "Radiation": [720],
        "AirTemperature": [29],
        "RelativeAirHumidity": [58],
        "Hour": [13],
        "Day": [15],
        "Month": [6]

    })

    result = predict(sample)

    print(result)