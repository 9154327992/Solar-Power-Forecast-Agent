# ============================================================
# database.py
# SQLite Database Operations
# ============================================================

import sqlite3
from contextlib import closing

DATABASE_NAME = "solar_predictions.db"


# ============================================================
# Database Connection
# ============================================================

def get_connection():
    """
    Create and return a SQLite connection.
    """
    return sqlite3.connect(DATABASE_NAME)


# ============================================================
# Initialize Database
# ============================================================

def initialize_database():
    """
    Create predictions table if it does not exist.
    """

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS predictions(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            temperature REAL,

            humidity REAL,

            pressure REAL,

            wind_speed REAL,

            cloud_cover REAL,

            prediction REAL,

            efficiency REAL,

            generation_level TEXT

        )

        """)

        conn.commit()


# ============================================================
# Insert Prediction
# ============================================================

def insert_prediction(data):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO predictions(

            timestamp,

            temperature,

            humidity,

            pressure,

            wind_speed,

            cloud_cover,

            prediction,

            efficiency,

            generation_level

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        """,

        (

            data["timestamp"],

            data["temperature"],

            data["humidity"],

            data["pressure"],

            data["wind_speed"],

            data["cloud_cover"],

            data["prediction"],

            data["efficiency"],

            data["generation_level"]

        )

        )

        conn.commit()


# ============================================================
# Get Prediction History
# ============================================================

def get_history():

    with closing(get_connection()) as conn:

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM predictions

        ORDER BY id DESC

        """)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]


# ============================================================
# Get Prediction By ID
# ============================================================

def get_prediction(prediction_id):

    with closing(get_connection()) as conn:

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM predictions

        WHERE id=?

        """,

        (prediction_id,)

        )

        row = cursor.fetchone()

        if row:

            return dict(row)

        return None


# ============================================================
# Delete Prediction
# ============================================================

def delete_prediction(prediction_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(

            "DELETE FROM predictions WHERE id=?",

            (prediction_id,)

        )

        conn.commit()


# ============================================================
# Delete All Predictions
# ============================================================

def clear_history():

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(

            "DELETE FROM predictions"

        )

        conn.commit()


# ============================================================
# Database Statistics
# ============================================================

def database_statistics():

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(

            "SELECT COUNT(*) FROM predictions"

        )

        total_predictions = cursor.fetchone()[0]

        cursor.execute(

            "SELECT AVG(prediction) FROM predictions"

        )

        average_prediction = cursor.fetchone()[0]

        return {

            "total_predictions": total_predictions,

            "average_prediction":

                round(average_prediction, 2)

                if average_prediction

                else 0

        }


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    initialize_database()

    print("Database initialized successfully.")