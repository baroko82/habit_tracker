"""
This Module is for the database interactions. Creating the Database Table, Storing information and returning those
"""
import sqlite3


def create_tables(db):
    """
    This creates the 2 tables "HT_Habits" and "HT_Log" which store the Data from this application.

    HT_Habits consists of the columns/attributes: habit (which works as a primary key) , periodicity, category,
    creation_time, streak, and completion_time.
    HT_Log consists of columns/attributes: habit, completed, streak, and completion_time.

    :param db: is to maintain a connection with the chosen database
    """
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS HT_Habits (
               habit TEXT PRIMARY KEY , 
               periodicity TEXT,
               category TEXT,
               creation_time TEXT,
               streak INT,
               completion_time TEXT   
           )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS HT_Log (
            habit TEXT,
            completed BOOL,
            streak INT DEFAULT 0,
            completion_time TIME,
            FOREIGN KEY (habit) REFERENCES HT_Habits(habit)
        )''')
    db.commit()


def connect_database(name="HT.db"):
    """
    This function connects to the Database.

    :param name: is the name of the database which is created (if necessary) or connected with (default HT.db)
    :return: Returns the said database connection
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def add_habit(db, name, periodicity, category, creation_time, streak, completion_time=None):
    """
    This function is called to add habit information to the HT_Habits database.

    :param db: is to maintain a connection with the chosen database
    :param name: for the name of the habit
    :param periodicity: interval in which the habit has to be checked - in this case either daily, weekly, or monthly
    :param category: What kind of Category the habit belongs to, like sports, chore, duty
    :param creation_time: is the Time when habit was created
    :param streak: count of how many times the habit (if so) has been checked in according to its periodicity, Integer
    :param completion_time: optional value, the time the habit was checked as completed
    """
    cur = db.cursor()
    cur.execute("INSERT INTO HT_Habits VALUES(?, ?, ?, ?, ?, ?)",
                (name, periodicity, category,
                 creation_time, streak, completion_time))
    db.commit()


def update_log(db, name, is_completed, streak, completion_time):
    """
    Updates the habit_log database with the provided data.

    :param db: is to maintain a connection with the chosen database
    :param name: for the name of the habit
    :param is_completed: boolean value, true if habit completed
    :param streak: count of how many times the habit (if so) has been checked in according to its periodicity, Integer
    :param completion_time: optional value, the time the habit was checked as completed
        """
    cur = db.cursor()
    cur.execute("INSERT INTO HT_Log VALUES(?, ?, ?, ?)",
                (name, is_completed, streak, completion_time))
    db.commit()


def habit_exists(db, habit_name):
    """
    Function to check whether parameter-wise given habit does exist in the database

    :param db: is to maintain a connection with the chosen database
    :param habit_name: is the name of the searched habit
    :return: Bool Value, whether habit is in the database
    """
    cur = db.cursor()
    query = """SELECT * FROM HT_Habits WHERE habit = ?"""
    cur.execute(query, (habit_name,))
    data = cur.fetchone()
    return True if data is not None else False


def remove_habit(db, habit_name):
    """
    Deletes the parameter-wise given habit from the HT Database Tables

    :param db: is to maintain a connection with the chosen database
    :param habit_name: is the name of the habit to be deleted
    """
    cur = db.cursor()
    cur.execute(f"DELETE FROM HT_Habits WHERE habit == '{habit_name}';")
    db.commit()
    query = "DELETE FROM HT_Log WHERE habit = ?"
    cur.execute(query, (habit_name,))
    db.commit()


def get_streak_count(db, habit_name):
    """
    This function returns the current streak of the parameter-wise given habit.

    :param db: is to maintain a connection with the chosen database
    :param habit_name: for the name of the habit
    :return: returns the current streak count (Integer Value) of the given habit
    """
    cur = db.cursor()
    query = "SELECT streak FROM HT_Habits WHERE habit = ?"
    cur.execute(query, (habit_name,))
    streak_count = cur.fetchall()
    return streak_count[0][0]


def update_habit_streak(db, habit_name, streak, time=None):
    """
    This function updates the streak of a parameter-wise given habit.

    :param db: is to maintain connection with the chosen database
    :param habit_name: for the name of the habit
    :param streak: for the new streak value (INT) of the given habit
    :param time: a timestamp of the streak update
    """
    cur = db.cursor()
    query = "UPDATE HT_Habits SET streak = ?, completion_time = ? WHERE habit = ?"
    data = (streak, time, habit_name)
    cur.execute(query, data)
    db.commit()


def get_habit_completion_time(db, habit_name):
    """
    This function returns the last time when the habit was marked as completed.

    :param db: is to maintain connection with the chosen database
    :param habit_name: for the name of the habit
    :return: returns the last completion time
    """
    cur = db.cursor()
    query = "SELECT completion_time FROM HT_Habits WHERE habit = ?"
    cur.execute(query, (habit_name,))
    data = cur.fetchall()
    return data[0][0]


def fetch_habit_periodicity(db, habit_name):
    """
    This function returns the set periodicity of the parameter-wise given habit

    :param db: is to maintain connection with the database
    :param habit_name: for the name of the habit
    :return: returns the set periodicity of the habit
    """
    cur = db.cursor()
    query = "SELECT periodicity FROM HT_Habits WHERE habit =?"
    cur.execute(query, (habit_name,))
    data = cur.fetchall()
    return data[0][0]


def fetch_habits_as_choices(db):
    """
    Returns all the habits contained listed in the HT_Habits database table

    :param db: is to maintain a connection with the chosen database
    :return: Returns the list of habit names
    """
    cur = db.cursor()
    cur.execute("SELECT habit FROM HT_Habits")
    data = cur.fetchall()
    return [i[0].capitalize() for i in set(data)] if len(data) > 0 else None


def fetch_categories(db):
    """
    Returns all categories contained in the HT_Habits database table

    :param db: is to maintain a connection with the chosen database
    :return: returns a list of all categories within the HT_Habits Table
    """
    cur = db.cursor()
    cur.execute("SELECT category FROM HT_Habits")
    data = cur.fetchall()
    return [i[0].capitalize() for i in set(data)]


def delete_category(db, category_name):
    """
    Removes the parameter-wise given category from the HT_Habits database table
    And removes associated Habits from the HT_Log database table

    :param db: is to maintain a connection with the chosen database
    :param category_name: the Name of the category to be deleted
    """
    cur = db.cursor()
    cur.execute(f"SELECT habit FROM HT_Habits WHERE category == '{category_name}';")
    #Removing Habits from Log too, as Category removal does so on the Habits
    del_hab = cur.fetchall()
    for i in del_hab:
        cur.execute(f"DELETE FROM HT_Log where habit == '{del_hab.index(i)}';")

    cur.execute(f"DELETE FROM HT_Habits where category == '{category_name}';")
    db.commit()



def update_periodicity(db, habit_name, new_periodicity):
    """
    This function alters the periodicity of the parameter-wise given habit and resets logs
    of the same habit.

    :param db: is to maintain a connection with the chosen database
    :param habit_name: for the name of the habit
    :param new_periodicity: for the updated periodicity of given habit
    """
    cur = db.cursor()
    query = "UPDATE HT_Habits SET periodicity = ?, streak = 0, completion_time = NULL WHERE habit = ?"
    data = (new_periodicity, habit_name)
    cur.execute(query, data)
    db.commit()
    query = "DELETE FROM HT_Log WHERE habit = ?"
    cur.execute(query, (habit_name,))
    db.commit()
