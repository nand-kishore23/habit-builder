import unittest
import os
import json
import datetime
import sys

# Ensure main can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import HabitApp

class TestHabitApp(unittest.TestCase):
    def setUp(self):
        # Override the DB_FILE for testing to not overwrite actual user data
        self.test_db = "test_habit_data.json"
        HabitApp.DB_FILE = self.test_db
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.app = HabitApp()

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_initialization(self):
        self.assertEqual(self.app.habit["name"], "Study")
        self.assertEqual(self.app.habit["level"], 1)

    def test_draw_progress_bar(self):
        bar = self.app.draw_progress_bar(50, width=10)
        self.assertIn("50%", bar)

    def test_get_stats(self):
        self.app.habit["history"] = [datetime.date.today()]
        consist, streak, xp_to_next, xp_percent = self.app.get_stats()
        self.assertEqual(streak, 1)

if __name__ == '__main__':
    unittest.main()
