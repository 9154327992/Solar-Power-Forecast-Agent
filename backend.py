# ------------------------------------------------------------
# Import FastAPI Library
# ------------------------------------------------------------

from fastapi import FastAPI, HTTPException

# ------------------------------------------------------------
# Import Pydantic Library
# ------------------------------------------------------------

from pydantic import BaseModel

# ------------------------------------------------------------
# Import Pandas Library
# ------------------------------------------------------------

import pandas as pd

# ------------------------------------------------------------
# Import Joblib Library
# ------------------------------------------------------------

import joblib

# ------------------------------------------------------------
# Import SQLite Library
# ------------------------------------------------------------

import sqlite3

# ------------------------------------------------------------
# Import Date and Time Library
# ------------------------------------------------------------

from datetime import datetime

# ============================================================
# Create FastAPI Application
# ============================================================

app = FastAPI(

    title="Solar Power Forecast API",

    description="FastAPI Backend for Solar Power Forecast Agent",

    version="1.0"

)

# ============================================================
# Load Machine Learning Model
# ============================================================

try:

    model = joblib.load(

        "model.pkl"

    )

    scaler = joblib.load(

        "scaler.pkl"

    )

    print("Model and scaler loaded successfully.")

except Exception as e:

    print("Model loading failed.")

    print(e)

    raise e

# ============================================================
# Create SQLite Database
# ============================================================

def create_database():

    conn = sqlite3.connect(

        "prediction_records.db"

    )

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS predictions(

        prediction_date TEXT,

        prediction_time TEXT,

        predicted_power REAL,

        generation_level TEXT,

        efficiency REAL

    )

    """)

    conn.commit()

    conn.close()

# Create database

create_database()

# ============================================================
# Input Data Model
# ============================================================

class SolarInput(BaseModel):

    wind: float

    sunshine: float

    pressure: float

    radiation: float

    temperature: float

    humidity: float

    hour: int

    day: int

    month: int

# ============================================================
# Forecast Solar Power API
# ============================================================

@app.post("/forecast")

def forecast(data: SolarInput):

    try:

        # ----------------------------------------------------
        # Create Input DataFrame
        # ----------------------------------------------------

        input_data = pd.DataFrame({

            "WindSpeed": [data.wind],

            "Sunshine": [data.sunshine],

            "AirPressure": [data.pressure],

            "Radiation": [data.radiation],

            "AirTemperature": [data.temperature],

            "RelativeAirHumidity": [data.humidity],

            "Hour": [data.hour],

            "Day": [data.day],

            "Month": [data.month]

        })

        # ----------------------------------------------------
        # Scale Input Data
        # ----------------------------------------------------

        scaled_data = scaler.transform(

            input_data

        )

        # ----------------------------------------------------
        # Predict Solar Power
        # ----------------------------------------------------

        prediction = float(

            model.predict(

                scaled_data

            )[0]

        )

        # ----------------------------------------------------
        # Determine Generation Level
        # ----------------------------------------------------

        if prediction >= 5000:

            level = "Excellent 🌞"

        elif prediction >= 2000:

            level = "High ☀"

        elif prediction >= 500:

            level = "Moderate ⛅"

        else:

            level = "Low 🌙"

        # ----------------------------------------------------
        # Calculate Efficiency
        # ----------------------------------------------------

        efficiency = round(

            (prediction / 7701) * 100,

            2

        )

        efficiency = max(

            0,

            min(

                efficiency,

                100

            )

        )

        # ----------------------------------------------------
        # AI Recommendation
        # ----------------------------------------------------

        if level == "Excellent 🌞":

            recommendation = (

                "Excellent solar generation expected. Charge batteries and export surplus electricity."

            )

        elif level == "High ☀":

            recommendation = (

                "High solar generation expected. Use solar energy for household loads."

            )

        elif level == "Moderate ⛅":

            recommendation = (

                "Moderate solar generation expected. Operate appliances efficiently."

            )

        else:

            recommendation = (

                "Low solar generation expected. Use battery backup if required."

            )

        # ----------------------------------------------------
        # AI Insight
        # ----------------------------------------------------

        if level == "Excellent 🌞":

            insight = "Excellent weather conditions detected."

        elif level == "High ☀":

            insight = "Good weather conditions detected."

        elif level == "Moderate ⛅":

            insight = "Average weather conditions detected."

        else:

            insight = "Poor weather conditions detected."

        # ----------------------------------------------------
        # Save Prediction
        # ----------------------------------------------------

        conn = sqlite3.connect(

            "prediction_records.db"

        )

        cursor = conn.cursor()

        cursor.execute(

            """

            INSERT INTO predictions

            VALUES (?,?,?,?,?)

            """,

            (

                datetime.now().strftime("%Y-%m-%d"),

                datetime.now().strftime("%H:%M:%S"),

                round(prediction, 2),

                level,

                efficiency

            )

        )

        conn.commit()

        conn.close()

        # ----------------------------------------------------
        # Return JSON Response
        # ----------------------------------------------------

        return {

            "prediction": prediction,

            "level": level,

            "efficiency": efficiency,

            "recommendation": recommendation,

            "insight": insight

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
    
# ============================================================
# Prediction History API
# ============================================================

@app.get("/history")

def get_history():

    try:

        # Connect to SQLite database

        conn = sqlite3.connect(

            "prediction_records.db"

        )

        # Read prediction history

        history = pd.read_sql(

            "SELECT * FROM predictions",

            conn

        )

        # Close database

        conn.close()

        # Return history as JSON

        return history.to_dict(

            orient="records"

        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# ============================================================
# Home API
# ============================================================

@app.get("/")

def home():

    return {

        "message": "Solar Power Forecast API is running successfully.",

        "framework": "FastAPI",

        "model": "XGBoost",

        "database": "SQLite",

        "version": "1.0"

    }


# ============================================================
# Health Check API
# ============================================================

@app.get("/health")

def health():

    return {

        "status": "Healthy",

        "api": "Running",

        "database": "Connected",

        "model": "Loaded"

    }