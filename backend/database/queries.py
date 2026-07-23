# ============================================================
# queries.py
# Database Query Manager
# ============================================================

from backend.database.database import get_connection


class DatabaseQueries:
    """
    Handles common database queries.
    """

    # ========================================================
    # Prediction Queries
    # ========================================================

    def get_all_predictions(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM predictions
            ORDER BY timestamp DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows

    def get_latest_prediction(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM predictions
            ORDER BY timestamp DESC
            LIMIT 1
        """)

        row = cursor.fetchone()
        conn.close()

        return row

    def delete_prediction(self, prediction_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM predictions
            WHERE id = ?
        """, (prediction_id,))

        conn.commit()
        conn.close()

    # ========================================================
    # User Queries
    # ========================================================

    def get_user(self, username):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()
        conn.close()

        return user

    def get_all_users(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, email, created_at
            FROM users
            ORDER BY created_at DESC
        """)

        users = cursor.fetchall()
        conn.close()

        return users

    # ========================================================
    # Statistics
    # ========================================================

    def prediction_count(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM predictions
        """)

        count = cursor.fetchone()[0]
        conn.close()

        return count

    def user_count(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
        """)

        count = cursor.fetchone()[0]
        conn.close()

        return count


# Global instance
queries = DatabaseQueries()