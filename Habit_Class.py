"""
This Module contains the Habit Class for the Habit Tracker. Alongside constructor and functions with it
"""
import Habit_Tracker_Database as htdb
from datetime import datetime


class Habit:
    """
        Habit class - for having different habits (objects)
    """

    def __init__(self, name: str = None, periodicity: str = None, category: str = None, database="HT_weeks.db"):
        """
        Parameters:

        name : String Type, optional - The Name of the Habit (default = None)
        periodicity : String Type, optional - Period of Habit (daily/weekly/monthly) (default = None)
        category : String Type, optional - The Category of the Habit (like e.g. Chore, Duty, Sports) (default = None)
        database: String Type, optional - Connection to a database (default is HT.db) - Change for Tests
        (in Habit_Tracker_Database.connect_database function too)
        """

        self.name = name
        self.periodicity = periodicity
        self.category = category
        self.db = htdb.connect_database(database)
        self.streak = 0
        self.current_time = datetime.now().strftime("%m/%d/%Y %H:%M")

    def add(self):
        """
        Adds Habit to the Database Table "HT_Habits" and updates the Table "HT_Log".
        """
        if htdb.habit_exists(self.db, self.name) is False:
            htdb.add_habit(self.db, self.name, self.periodicity, self.category, self.current_time, self.streak)
            htdb.update_log(self.db, self.name, False, 0, self.current_time)
            print(f"\n The Habit: '{self.name.capitalize()}' with the Periodicity: '{self.periodicity.capitalize()}' "
                  f"has been added with the Category: '{self.category.capitalize()}' .\n")
        else:
            print("\nThis Habit already exists. You should pick another or rename it (e.g. Joggingdaily, Joggingweekly).\n")

    def remove(self):
        """
        Removes Habit from the Database Table "HT_Habits".
        """
        htdb.remove_habit(self.db, self.name)
        print(f"\nThe Habit: '{self.name.capitalize()}' has been removed.\n")

    def increment_streak(self):
        """
        Gets the current habit streak from database and increases it by 1.
        """
        self.streak = htdb.get_streak_count(self.db, self.name)
        self.streak += 1

    def update_streak(self):
        """
        Calls increment_streak()-function and updates the Database Entry in both HT_Habits and HT_Log
        """
        self.increment_streak()
        htdb.update_habit_streak(self.db, self.name, self.streak, self.current_time)
        htdb.update_log(self.db, self.name, True, htdb.get_streak_count(self.db, self.name), self.current_time)
        print(f"\n You kept it going! The new streak for Habit: '{self.name.capitalize()}' is {self.streak}\n")

    def mark_as_completed(self):
        """
        This function's purpose is the mark habits as completed.

        To do so, it checks the periodicity of the habit and calls a relevant method to verify
        whether the streak is due for being incremented or not - all depending on the day/week/month of the habit.
        Upon a broken streak it adds the reset habit to the log the same way as new habits are logged like
        and then adds an entry to the log starting the new streak, making it easier to see
        """

        # Streak Tracker & Assignment - Periodicity: Daily
        if htdb.fetch_habit_periodicity(self.db, self.name) == "daily":
            if self.daily_habit_streak_verification() == 0:
                print("\n This Habit has been completed Today! Check in Tomorrow, once you've completed it\n")
            elif self.daily_habit_streak_verification() == 1:
                self.update_streak()
            else:
                self.reset_streak()
                self.update_streak()

        # Streak Tracker & Assignment - Periodicity: Weekly
        elif htdb.fetch_habit_periodicity(self.db, self.name) == "weekly":
            if self.weekly_habit_streak_verification() == 1:
                print("\n Woah there, Champ! You've completed this Habit this week already. Be sure to keep it up and check in next week\n")
            elif self.weekly_habit_streak_verification() == 2:
                self.update_streak()
            else:
                self.reset_streak()
                self.update_streak()

        # Streak Tracker & Assignment - Periodicity: Monthly
        elif htdb.fetch_habit_periodicity(self.db, self.name) == "monthly":
            if self.monthly_habit_streak_verification() == 0:
                print("\n Yeah. I Know it's hard to keep track of all the Habits, that's what I'm here for. Since you completed this Habit this Month already, i suggest checking in next month again\n")
            elif self.monthly_habit_streak_verification() == 1:
                self.update_streak()
            else:
                self.reset_streak()
                self.update_streak()

    def daily_habit_streak_verification(self):
        """
        This functions returns the number of day(s) that have passed since the last time the habit has been completed
        :return date.days: Number of day(s) that have passed since the last completion of the habit
        """
        last_complete = htdb.get_habit_completion_time(self.db, self.name)
        previous_streak = htdb.get_streak_count(self.db, self.name)
        if previous_streak == 0 or last_complete is None:
            return 1
        else:
            today = self.current_time
            date = datetime.strptime(today[:10], "%m/%d/%Y") - datetime.strptime(last_complete[:10], "%m/%d/%Y")
            return date.days

    def weekly_habit_streak_verification(self):
        """
        This functions returns the number of week(s) that have passed since the last time the habit has been completed
        :return date.weeks: Number of week(s) that have passed since the last completion of the habit
        """
        last_complete = htdb.get_habit_completion_time(self.db, self.name)
        previous_streak = htdb.get_streak_count(self.db, self.name)
        if (previous_streak == 0) or (last_complete is None):
            return 2
        else:
            today = self.current_time
            delta = datetime.strptime(today[:10], "%m/%d/%Y") - datetime.strptime(last_complete[:10], "%m/%d/%Y")
            #More than 14 Days (2 Weeks) aka true with broken streak
            if (delta.days + 1) > 14:
                return 3
            #More than 7 Days (1 Week) aka true for checking in
            elif (delta.days + 1) > 7:
                return 2
            #Less than 7 Days (1 Week) aka already checked
            else:
                return 1

    def monthly_habit_streak_verification(self):
        """
        This functions returns the number of month(s) that have passed since the last time the habit has been completed
        :return date.months: Number of month(s) that have passed since the last completion of the habit
        """
        last_complete = htdb.get_habit_completion_time(self.db, self.name)
        previous_streak = htdb.get_streak_count(self.db, self.name)
        if (previous_streak == 0) or (last_complete is None):
            return 1
        else:
            current_month = self.current_time
            month = int(current_month[:2]) - int(last_complete[:2])
            return month

    def reset_streak(self):
        """
        This functions resets a habit's streak back to 0
        It also updates the Tables "HT_Habits" and "HT_Log" from the database.
        """
        self.streak = 0
        htdb.update_habit_streak(self.db, self.name, self.streak, self.current_time)
        htdb.update_log(self.db, self.name, False, htdb.get_streak_count(self.db, self.name), self.current_time)
        print("\nThe Streak has been broken!")
        print(f"Your new streak for Habit: '{self.name.capitalize()}' has been reseted to {self.streak}.\n")

    def delete_category(self):
        """
        Deletes the category and all of its assigned habits from "HT_Habits" Database Table
        """
        htdb.delete_category(self.db, self.category)
        print(f"\nThe Category '{self.category.capitalize()}' has been removed.\n")


    def change_periodicity(self):
        """
        Alters a habit's periodicity and updates the log.
        """
        htdb.update_periodicity(self.db, self.name, self.periodicity)
        htdb.update_log(self.db, self.name, False, 0, self.current_time)
        print(f"\n The Periodicity of Habit: '{self.name.capitalize()}' is now: '{self.periodicity.capitalize()}'\n")
