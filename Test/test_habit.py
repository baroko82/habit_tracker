import pytest
from Habit_Class import Habit
import Habit_Tracker_Database as htdb
import os
from freezegun import freeze_time



@pytest.fixture(scope='module')
def db():
    db = htdb.connect_database("habit_test.db")
    yield db
    db.close()



def test_add(db):
    habit = Habit("study", "daily", "job", database="habit_test.db")
    habit.add()
    habit_2 = Habit("tea", "daily", "pleasure", database="habit_test.db")
    habit_2.add()
    assert htdb.habit_exists(db, "study")
    assert htdb.habit_exists(db, "tea")


def test_remove(db):
    assert htdb.habit_exists(db, "study") is True
    habit = Habit("study", "daily", "job", database="habit_test.db")
    habit.remove()
    assert htdb.habit_exists(db, "study") is False


def test_delete_category(db):
    assert len(htdb.fetch_categories(db)) == 1
    habit_3 = Habit("run", "daily", "sport", database="habit_test.db")
    habit_3.add()
    assert len(htdb.fetch_categories(db)) == 2
    habit_3.delete_category()
    assert len(htdb.fetch_categories(db)) == 1


def test_change_periodicity(db):
    assert htdb.fetch_habit_periodicity(db, "tea") == "daily"
    habit_2 = Habit("tea", "weekly", database="habit_test.db")
    habit_2.change_periodicity()
    assert htdb.fetch_habit_periodicity(db, "tea") == "weekly"


# Now some Timey-Wimey Stuff, making use of the freezegun library to alter time for testing, YYYY-MM-DD  as Time Format
@freeze_time("2024-02-01")
#Habits (d)aily, (w)eekly, (m)onthly
def test_add_custom_habits(db):
    habit_d = Habit("paint", "daily", "fun", database="habit_test.db")
    habit_d.add()
    habit_w = Habit("dennycrane", "weekly", "meeting", database="habit_test.db")
    habit_w.add()
    habit_m = Habit("payrent", "monthly", "duty", database="habit_test.db")
    habit_m.add()
    assert htdb.habit_exists(db, "paint")


@freeze_time("2024-02-01")
def test_mark_daily_habit_as_completed(db):
    habit_d = Habit("paint", "daily", "fun", database="habit_test.db")
    habit_d.mark_as_completed()
    assert htdb.get_streak_count(db, "paint") == 1


@freeze_time("2024-02-01")
def test_mark_daily_habit_as_completed_twice(db):
    habit_d = Habit("paint", "daily", "fun", database="habit_test.db")
    habit_d.mark_as_completed()
    assert htdb.get_streak_count(db, "paint") != 2


@freeze_time("2024-02-02")
def test_mark_daily_habit_as_completed_next_day(db):
    habit_d = Habit("paint", "daily", "fun", database="habit_test.db")
    habit_d.mark_as_completed()
    assert htdb.get_streak_count(db, "paint") == 2


@freeze_time("2024-02-01")
def test_mark_weekly_habit_as_completed(db):
    assert htdb.get_streak_count(db, "dennycrane") == 0
    habit_w = Habit("dennycrane", "weekly", "meeting", database="habit_test.db")
    habit_w.mark_as_completed()
    assert htdb.get_streak_count(db, "dennycrane") == 1


@freeze_time("2024-02-02")
def test_mark_weekly_habit_as_completed_same_week(db):
    habit_w = Habit("dennycrane", "weekly", "meeting", database="habit_test.db")
    habit_w.mark_as_completed()
    assert htdb.get_streak_count(db, "dennycrane") != 2


@freeze_time("2024-02-08")
def test_mark_weekly_habit_as_completed_next_week(db):
    habit_w = Habit("dennycrane", "weekly", "meeting", database="habit_test.db")
    habit_w.mark_as_completed()
    assert htdb.get_streak_count(db, "dennycrane") == 2


@freeze_time("2024-02-01")
def test_mark_monthly_habit_as_completed(db):
    habit_m = Habit("payrent", "monthly", "duty", database="habit_test.db")
    habit_m.mark_as_completed()
    assert htdb.get_streak_count(db, "payrent") == 1


@freeze_time("2024-02-15")
def test_mark_monthly_habit_as_completed_same_month(db):
    habit_m = Habit("payrent", "monthly", "duty", database="habit_test.db")
    habit_m.mark_as_completed()
    assert htdb.get_streak_count(db, "payrent") != 2


@freeze_time("2024-03-01")
def test_mark_monthly_habit_as_completed_month_later(db):
    habit_m = Habit("payrent", "monthly", "duty", database="habit_test.db")
    habit_m.mark_as_completed()
    assert htdb.get_streak_count(db, "payrent") == 2


try:
    os.remove("habit_test.db")
except OSError:
    pass

