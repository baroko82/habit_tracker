"""
This Analytics Moduls collects, evaluates and presents the Data

It is called upon, when the user picks either "Listing Habits" or "Analytics Module".
"""

from Habit_Tracker_Database import connect_database
from rich.console import Console
from rich.table import Table


def data_all_habits(db) -> list:
    """
    Does a Query to gain a list of all habits stored in HT_Habits database table.

    :param db: for connection with the database.
    :return: the list of all habits
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM HT_Habits")
    content = cur.fetchall()
    return content


def data_single_habit(db, habit_name) -> list:
    """
    Does a Query to gain the data of a single chosen habit stored in HT_Habits database table.

    :param db: for connection with the database
    :param habit_name: which Habit is being asked about
    :return: Data of selected habit
    """
    cur = db.cursor()
    query = "SELECT * FROM HT_Habits WHERE habit = ?"
    cur.execute(query, (habit_name,))
    content = cur.fetchall()
    return content


def data_periodicity_habits(db, periodicity) -> list:
    """
    Does a Query to gain a list of all habits with specified periodicity stored in HT_Habits database table.

    :param db: for connection with the database
    :param periodicity: which periodicity of habits with wanted
    :return: list of all habits with specified periodicity
    """
    cur = db.cursor()
    query = "SELECT * FROM HT_Habits WHERE periodicity = ?"
    cur.execute(query, (periodicity,))
    content = cur.fetchall()
    return content


def longest_streak(db, habit_name) -> int:
    """
    Does a Query to gain the longest streak achieved for a chosen habits from the HT_Log database table.

    :param db: for connection with the database
    :param habit_name: which Habit's longest Streak is asked for
    :return: longest streak of given habit
    """
    cur = db.cursor()
    query = "SELECT MAX(streak) FROM HT_Log WHERE habit = ?"
    cur.execute(query, (habit_name,))
    data = cur.fetchone()
    return data[0]


def habit_log(db, habit_name) -> list:
    """
    Does a Query to a habit's Log Data from HT_Log database table.

    :param db: for connection with the database
    :param habit_name: which Habit's data is asked for
    :return: The data of given habit
    """
    cur = db.cursor()
    query = "SELECT * FROM HT_Log WHERE habit = ?"
    cur.execute(query, (habit_name,))
    content = cur.fetchall()
    return content


# Creating output "table" for just Habits depending on the periodicity
def list_habits_data(periodicity=None):
    """
    Displays the Habit's Data (Name, Periodicity, Category and Creation Date/Time) in a "table"

    The Data is collected from the database and then looped through.
    If a parameter for the periodicity is given, it will only display those fitting the parameter.
    If there is none given, all data is being presented

    :param periodicity: Choice of Habits with which Periodicity shall be displayed, default none equals ALL
    """
    db = connect_database()
    if periodicity is not None:
        data = data_periodicity_habits(db, periodicity)
    else:
        data = data_all_habits(db)
    if len(data) > 0:
        console = Console()

        table = Table(show_header=True, header_style="light_sea_green")
        table.add_column("Name", style="dim", width=12)
        table.add_column("Periodicity")
        table.add_column("Category", justify="right")
        table.add_column("Created: Date/Time", justify="right")
        for row in data:
            #From Left to Right: Name/Periodicity/Streak/Creation Time
            table.add_row(row[0].capitalize(), row[1].capitalize(), row[2].capitalize(), row[3].capitalize())
        console.print(table)

    else:
        print("\nThere is no Habit with that periodicity! :( You might add one with the Add Habit Function\n")


# Creating output "table" for Habit's Streak depending on the Habit
def list_habit_streak_data(habit=None):
    """
    Displays the (given) Habit's Data (Name, Periodicity, Completion Time and Current Streak / Longest Streak) in a "table"

    The Data is collected from the database and then looped through.
    If a parameter for the habit is given, it will only display those fitting the parameter alongside it's longest streak.
    If there is none given, all habits will be presented with their current streak

    :param habit: Choice of Habit's Streak to be displayed. Default none equals all habits
    """

    db = connect_database()
    if habit is None:
        data = data_all_habits(db)
    else:
        data = data_single_habit(db, habit)
    if len(data) > 0:
        console = Console()

        table = Table(show_header=True, header_style="light_sea_green")
        table.add_column("Name", style="dim", width=12)
        table.add_column("Periodicity")
        table.add_column("Completion Time", justify="right")
        table.add_column("Current Streak" if habit is None else "Longest Streak", justify="left")
        for row in data:
            period = " Day(s)" if row[1] == "daily" else (" Week(s)" if row[1] == "weekly" else " Month(s)")
            # From Left to Right: Name/Periodicity/Completion Time/Current or Longest Streak
            table.add_row(row[0].capitalize(), row[1].capitalize(),
                          row[5] if row[5] is not None else "--/--/-- --:--",
                          str(row[4]) + period if habit is None else str(longest_streak(db, habit)) + period)
        console.print(table)

    else:
        print("\nThere are no Habits! :( You might add one with the Add Habit Function!\n")


# Creating output "table" for Habit's Log
def list_habit_logged_data(name_of_habit):
    """
        Displays the (given) Habit's Log (Name, Completed, Streak, Logged at) in a "table"
        The Data is collected from the database and then looped through in order to display it

        :param name_of_habit: Habit's Name chosen to be displayed
        """
    db = connect_database()
    data = habit_log(db, name_of_habit)
    console = Console()

    if len(data) > 0:
        table = Table(show_header=True, header_style="light_sea_green")
        table.add_column("Name", style="dim", width=12)
        table.add_column("Completed")
        table.add_column("Streak", justify="center")
        table.add_column("Logged at", justify="right")
        for row in data:
            # From Left to Right: HabitName/ Complete? / Streak / Logged
            table.add_row(row[0].capitalize(), "[green]True[/green]" if row[1] == 1 else "[red]False[/red]", str(row[2]), row[3])
        console.print(table)
    else:
        print("There is no Record for the given Habit! Try another or use the Add Habit Function")


# Creating output "table" for all Habits of a category
def list_habits_category(category):
    """
    Displays the Habit's Data (Name, Periodicity, Category and "Creation" Date/Time) of the same category  in a "table"

    The Data is collected from the database and then looped through.

    :param category: Choice of Habits of which Category shall be displayed
    """

    db = connect_database()
    cur = db.cursor()
    query = "SELECT * FROM HT_Habits WHERE category = ?"
    cur.execute(query, (category,))
    data = cur.fetchall()

    if len(data) > 0:
        console = Console()

        table = Table(show_header=True, header_style="light_sea_green")
        table.add_column("Name", style="dim", width=12)
        table.add_column("Periodicity")
        table.add_column("Category", justify="right")
        table.add_column("Created: Date/Time", justify="right")
        for row in data:
            # From Left to Right: Name/Periodicity/Streak/Creation Time
            table.add_row(row[0].capitalize(), row[1].capitalize(), row[2].capitalize(), row[3].capitalize())
        console.print(table)

    else:
        print("\nThere are no Habit of the Category! :( You might add one with the Add Habit Function\n")
