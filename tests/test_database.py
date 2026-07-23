# ============================================================
# test_database.py
# ============================================================

import unittest

from backend.database.database import (
    initialize_database,
    insert_prediction,
    get_history,
    database_statistics
)


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Initialize the database before running tests.
        """
        initialize_database()

    def test_insert_prediction(self):
        """
        Test inserting a prediction into the database.
        """

        prediction = {
            "city": "Kathmandu",
            "prediction": 5420.35,
            "level": "High",
            "efficiency": 70.38,
            "recommendation": "Excellent solar generation expected."
        }

        insert_prediction(prediction)

        history = get_history()

        self.assertGreater(len(history), 0)

    def test_database_statistics(self):
        """
        Test database statistics.
        """

        stats = database_statistics()

        self.assertIsInstance(stats, dict)
        self.assertIn("total_predictions", stats)

    def test_history(self):
        """
        Test retrieving prediction history.
        """

        history = get_history()

        self.assertIsInstance(history, list)


if __name__ == "__main__":
    unittest.main()