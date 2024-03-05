import Habit_Tracker_Database as htdb
import os


class TestDatabase:
    """
    Test Database class contains methods for testing the important functions of Habit_Tracker_Database module
    """
    def setup_method(self):
        self.db = htdb.connect_database("db_test.db")
        # Creating 6 habits with different 4 categories and each periodicity at least once
        htdb.add_habit(self.db, "tea", "daily", "pleasure", "02/01/2024 13:37", 0)
        htdb.add_habit(self.db, "cake", "daily", "pleasure", "02/02/2024 13:37", 0)
        htdb.add_habit(self.db, "bath", "daily", "pleasure", "02/01/2024 13:37", 0)
        htdb.add_habit(self.db, "soccer", "weekly", "sport", "02/01/2024 19:04", 0)
        htdb.add_habit(self.db, "friends", "monthly", "meeting", "02/01/2024 11:11", 0)
        htdb.add_habit(self.db, "coffee", "daily", "addiction", "01/01/2022 13:00", 0)

    def test_fetch_habits_as_choices(self):
        assert len(htdb.fetch_habits_as_choices(self.db)) == 6

    def test_fetch_categories(self):
        assert len(htdb.fetch_categories(self.db)) == 4

    def test_remove_habit(self):
        htdb.remove_habit(self.db, "coffee")
        assert htdb.habit_exists(self.db, "coffee") is False
        assert len(htdb.fetch_habits_as_choices(self.db)) == 5

    def test_update_periodicity(self):
        htdb.update_periodicity(self.db, "friends", "weekly")
        assert htdb.fetch_habit_periodicity(self.db, "friends") == "weekly"

    def test_update_habit_streak(self):
        htdb.update_habit_streak(self.db, "tea", 1, "02/02/2024 17:00")
        assert htdb.get_streak_count(self.db, "tea") == 1

    def teardown_method(self):
        self.db.close()
        os.remove("db_test.db")
