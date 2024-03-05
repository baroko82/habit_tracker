import questionary as q
import Habit_Class
import Habit_Tracker_QnA as qna
import Habit_Tracker_Analytics


#  CLI Interface
def menu():
    """
    Simple Command Line Interface, Main Menu
    """
    # The Menu for the User to Choose From
    print("\n================ MAIN = MENU =================")
    pick = q.select(
        "Make your Choice",
        choices=[
            "Addition or Removal",
            "Complete Habit",
            "Change the Periodicity of a Habit",
            "Listing Habits",
            "Analytics Module",
            "End Program"
            ]).ask()
    print("==============================================\n")
    
    if pick == "Addition or Removal":
        # Sub Picks According to User's Choice
        print("=== ADDITION OR REMOVAL MENU ===")
        pick_2 = q.select(
            "Make your Choice",
            choices=[
                "Add a Habit",
                "Remove a Habit",
                "Delete a Category",
                "Return to Main Menu",
            ]).ask()
        print("================================")
        if pick_2 == "Add a Habit":
            habit_name = qna.habit_name()
            habit_periodicity = qna.habit_periodicity()
            #Asking existing Category or new one
            cat_ask = q.select("Category Choice ",
            choices=["Use existing Category",
                     "Create New Category",
            ]).ask()
            if cat_ask == "Use existing Category":
                try:
                    habit_category = qna.defined_categories()
                # It may raise the ValueError if the database does not have any categories stored!
                except ValueError:
                    print(
                        "\nThe Database has no categories stored.\n")
                    print("Since no category was found, Creating a new one")
                    habit_category = qna.habit_category()

            elif cat_ask == "Create New Category":
                habit_category = qna.habit_category()
            habit = Habit_Class.Habit(habit_name, habit_periodicity, habit_category)
            habit.add()

        elif pick_2 == "Remove a Habit":
            try:
                habit_name = qna.habits_from_db()
            # Might raise ValueError if no habit in the database!
            except ValueError:
                print("\nThe Database has no habits stored. You should add a Habit with the 'Add habit' function first.\n")
            else:
                habit = Habit_Class.Habit(habit_name)
                if qna.habit_delete_confirmation(habit_name):
                    habit.remove()
                else:
                    print("\nIf you change your mind, come back again\n")

        elif pick_2 == "Delete a Category":
            try:
                habit_category = qna.defined_categories()
            # It may raise the ValueError if the database does not have any categories stored!
            except ValueError:
                print("\nThe Database has no categories stored. You should define a category using 'Add habit' function first.\n")
            else:
                if qna.category_delete_confirmation():
                    habit = Habit_Class.Habit(category=habit_category)
                    habit.delete_category()
                else:
                    print("\nIf you change your mind, come back again\n")

        elif pick_2 == "Return to Main Menu":  #
            print("--- Returning to Main Menu ---\n")
            menu()

    elif pick == "Complete Habit":
        try:
            habit_name = qna.habits_from_db()
        # Might raise ValueError if no habit in the database!
        except ValueError:
            print("\nThe Database has no habits stored. You should add a Habit with the 'Add habit' function first.\n")
        else:
            habit = Habit_Class.Habit(habit_name)
            habit.mark_as_completed()

    elif pick == "Change the Periodicity of a Habit":
        try:
            habit_name = qna.habits_from_db()
            # Might raise ValueError if no habit in the database!
        except ValueError:
            print("\nThe Database has no habits stored. You should add a Habit with the 'Add habit' function first.\n")
        else:
            new_periodicity = qna.habit_periodicity()
            if qna.periodicity_change_confirmed():
                habit = Habit_Class.Habit(habit_name, new_periodicity)
                habit.change_periodicity()
            else:
                print(f"\nThe Periodicity of Habit {habit_name} stays the same. Come back, if you want to change that.\n")

    elif pick == "Listing Habits":
        # Gaining the List from the Habit_Tracker_QnA Module
        print("=== OPTIONS FOR LISTING HABITS ===")
        pick_2 = qna.show_period_choices()
        if pick_2 == "List ALL Habits":
            Habit_Tracker_Analytics.list_habits_data()

        elif pick_2 == "List DAILY Habits":
            Habit_Tracker_Analytics.list_habits_data("daily")

        elif pick_2 == "List WEEKLY Habits":
            Habit_Tracker_Analytics.list_habits_data("weekly")

        elif pick_2 == "List MONTHLY Habits":
            Habit_Tracker_Analytics.list_habits_data("monthly")

        elif pick_2 == "List Habits of Category":
            try:
                habit_category = qna.defined_categories()
            # It may raise the ValueError if the database does not have any categories stored!
            except ValueError:
                print(
                    "\nThe Database has no categories stored. You should define a category using 'Add habit' function first.\n")
            else:
                Habit_Tracker_Analytics.list_habits_category(category=habit_category)


        elif pick_2 == "Return to Main Menu":
            print("--- Returning to Main Menu ---\n")
            menu()

    elif pick == "Analytics Module":
        # Gaining the Options available
        print("===== ANALYTIC ===== OPTIONS =====")
        pick_2 = qna.analytics_choices()
        if pick_2 == "List All Habit's Streaks":
            Habit_Tracker_Analytics.list_habit_streak_data()

        elif pick_2 == "List Longest Streak of Specific Habit":
            try:
                habit_name = qna.habits_from_db()
            # Might raise ValueError if no habit in the database!
            except ValueError:
                print(
                    "\nThe Database has no habits stored. You should add a Habit with the 'Add habit' function first.\n")
            else:
                Habit_Tracker_Analytics.list_habit_streak_data(habit_name)

        elif pick_2 == "List Streak Log of Specific Habit":
            try:
                habit_name = qna.habits_from_db()
            # Might raise ValueError if no habit in the database!
            except ValueError:
                print("\nThe Database has no habits stored. You should add a Habit with the 'Add habit' function first.\n")
            else:
                Habit_Tracker_Analytics.list_habit_logged_data(habit_name)

        elif pick_2 == "Return to Main Menu":
            print("--- Returning to Main Menu ---\n")
            menu()

    elif pick == "End Program":
        global x
        print("Goodbye - Thank you for using the Habit Tracker")
        x = False

# Starting the Main Loop and Greeting the User
print("\n\nWelcome to the Habit Tracker\n\n")
x = True
while x:
    menu()
