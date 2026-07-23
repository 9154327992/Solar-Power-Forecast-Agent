# ============================================================
# login.py
# User Login Authentication
# ============================================================

import sqlite3
import bcrypt

DATABASE_NAME = "solar_predictions.db"


# ============================================================
# Database Connection
# ============================================================

def get_connection():

    return sqlite3.connect(DATABASE_NAME)


# ============================================================
# Login User
# ============================================================

def login_user(username: str, password: str):

    """
    Authenticate user.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT password
        FROM users
        WHERE username=?
        """,

        (username,)

    )

    user = cursor.fetchone()

    conn.close()

    if user is None:

        return {

            "success": False,

            "message": "User not found."

        }

    stored_password = user[0]

    if bcrypt.checkpw(

        password.encode(),

        stored_password.encode()

    ):

        return {

            "success": True,

            "message": "Login successful."

        }

    return {

        "success": False,

        "message": "Incorrect password."

    }


# ============================================================
# Verify User Exists
# ============================================================

def user_exists(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT id FROM users WHERE username=?",

        (username,)

    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    result = login_user(

        "admin",

        "admin123"

    )

    print(result)