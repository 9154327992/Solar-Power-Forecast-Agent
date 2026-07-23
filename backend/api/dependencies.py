"""
Common dependencies used across the API.
"""

from typing import Generator

from backend.database.database import get_connection


def get_db() -> Generator:
    """
    Returns a database connection.
    """

    connection = get_connection()

    try:
        yield connection
    finally:
        connection.close()


def get_current_user():
    """
    Placeholder for JWT authentication.

    Will be implemented after login API.
    """

    return None