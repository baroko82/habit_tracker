"""
This Questions and Answer module helps with functions and user choice's via the questionary library.

It enables the user to enter names, choose periodicity and category when creating habits.
Displays the different options (menus, stored data) available - all with the help of the Habit_Tracker_Database module
Last but not least it asks user for confirmation when deleting/changing
"""

import questionary as q
from Habit_Tracker_Database import connect_database, fetch_categories, fetch_habits_as_choices


def habit_name():
    """
    Prompts the user the CLI to enter a name for the habit.

    The Habit's name must be alphabets only! No whitespaces or special
    characters like "_" or %, & are allowed.

    :return: Returns Name of Habit typed in by user
    """
    return q.text("Type in a Name for your Habit: ",
                   validate=lambda name: True if name.isalpha() and len(name) > 1
                   else "That Name is Invalid! Try Again - Alphabets Only, No Whitespace or Special Character!").ask().lower()


def habit_periodicity():
    """
    Presents the possible Choices of Periodicity to choose from.

    :return: Returns the chosen habit's periodicity
    """
    return q.select("Please pick a Periodicity for your Habit ",
                     choices=["Daily", "Weekly", "Monthly"]).ask().lower()


def habits_from_db():
    """
    Displays the habit names available in the database for the user to choose from.

    :return: Returns the chosen habit from the presented list
    :raises ValueError: It may raise the ValueError if the database does not have any habits stored
    """
    db = connect_database()
    list_of_habits = fetch_habits_as_choices(db)
    if list_of_habits is not None:
        print("=== HABITS TO PICK FROM ===")
        selection = q.select("Make your Choice ",
                         choices=sorted(list_of_habits)).ask().lower()
        print("===========================\n")
        return selection

    else:
        raise ValueError("The Database has no habits stored. You should add a Habit with the 'Add habit' function first.")


def show_period_choices():
    """
    Displays the list of periodicity available for the user to choose from.

    :return: Returns the Choice as String
    """

    choice = q.select("Make your Choice ",
                       choices=[
                           "List ALL Habits",
                           "List DAILY Habits",
                           "List WEEKLY Habits",
                           "List MONTHLY Habits",
                           "List Habits of Category",
                           "Return to Main Menu"
                       ]).ask()
    print("==================================\n")
    return choice


def analytics_choices():
    """
    Displays Options for Analysis to choose from.

    :return: Returns the Choice as String
    """
    choice = q.select("Make your Choice ",
                       choices=[
                           "List All Habit's Streaks",
                           "List Longest Streak of Specific Habit",
                           "List Streak Log of Specific Habit",
                           "Return to Main Menu"
                       ]).ask()
    print("==================================\n")
    return choice


def habit_delete_confirmation(habit_name_to_delete):
    """
    Displays the Question if the User wants to Delete the Habit.

    :return: Returns True if yes else returns False
    """
    return q.confirm(f"Are you sure that you want to remove Habit: '{habit_name_to_delete}' from the Database?").ask()


def habit_category():
    """
    Prompts the user the CLI to enter a name for the habit's category

    The catagory's name must be alphabets only! No whitespaces or special
    characters like "_" or %, & are allowed.

    :return: Returns the name of the category provided by the user
    """
    return q.text("Type in a the Name for your Category: ",
                   validate=lambda category: True if category.isalpha() and len(category) > 1
                   else "That Name is Invalid! Try Again - Alphabets Only, No Whitespace or Special Character!").ask().lower()


def defined_categories():
    """
    Presents all categories stored within the database table for the user to make a pick

    :return: Returns the chosen category from the presented list
    :raises ValueError: It may raise the ValueError if the database does not have any categories stored
    """
    db = connect_database()
    arr = fetch_categories(db)
    if len(arr) > 0:
        return q.select("Make your Choice ",
                         choices=sorted(arr)).ask().lower()
    else:
        raise ValueError("The Database has no categories stored. You should define a category using 'Add habit' function first. ")


def category_delete_confirmation():
    """
    Displays the Question if the User wants to Delete the Category

    :return: Returns True if yes else returns False
    """
    return q.confirm("WARNING: By removing this category, you are also removing all associated habits!!! Are you sure?").ask()


def periodicity_change_confirmed():
    """
    Displays the Question if the User wants to alter the Category

    :return: Returns True if yes else returns False
    """
    return q.confirm("WARNING: By Changing the periodicity of a habit, you are also resetting the streak!!! Are you sure?").ask()
