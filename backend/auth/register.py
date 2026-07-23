# ============================================================
# register.py
# User Registration
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
# Check Username
# ============================================================

def username_exists(username):

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
# Check Email
# ============================================================

def email_exists(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT id FROM users WHERE email=?",

        (email,)

    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists


# ============================================================
# Register User
# ============================================================

def register_user(

    username,

    email,

    password

):

    """
    Register a new user.
    """

    if username_exists(username):

        return {

            "success": False,

            "message": "Username already exists."

        }

    if email_exists(email):

        return {

            "success": False,

            "message": "Email already exists."

        }

    hashed_password = bcrypt.hashpw(

        password.encode(),

        bcrypt.gensalt()

    ).decode()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        INSERT INTO users(

            username,

            email,

            password

        )

        VALUES (?, ?, ?)

        """,

        (

            username,

            email,

            hashed_password

        )

    )

    conn.commit()

    conn.close()

    return {

        "success": True,

        "message": "Registration successful."

    }


# ============================================================
# Get User
# ============================================================

def get_user(username):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT id,

               username,

               email,

               created_at

        FROM users

        WHERE username=?

        """,

        (username,)

    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return dict(user)

    return None


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    result = register_user(

        "admin",

        "admin@gmail.com",

        "admin123"

    )

    print(result)

    print(get_user("admin"))