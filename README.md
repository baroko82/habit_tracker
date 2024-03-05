<!-- TABLE OF CONTENTS -->
# Table of Contents
- [Habit Tracker](#habit-tracker)
  * [Habit Tracker's Main Functions](#habit-tracker-main-functions)
  * [Streak Tracker](#streak-tracker)
- [Preparations](#preparations)
  * [Dependencies](#dependencies)
  * [Installing](#installing)
  * [Additional Packages for Testing](#packages-for-test)
  * [Starting Program](#start-program)
  * [Running Tests](#running-tests)

- [Usage](#usage)
  * [Addition or Removal](#addition-or-removal)
      - [1. Add a habit](#1-add-habit)
      - [2. Remove a Habit](#2-remove-habit)
      - [3. Delete a Category](#3-delete-category)
      - [4. Return to Main Menu](#4-return-to-main-menu)
  * [Complete Habit](#complete-habit)

  * [Change the Periodicity of a Habit](#change-periodicity)

  * [Listing Habits](#listing-habits)
      - [1. List ALL Habits](#1-list-all-habits)
      - [2. List DAILY Habits](#2-list-daily-habits)
      - [3. List WEEKLY Habits](#3-list-weekly-habits)
      - [4. List MONTHLY Habits](#4-list-monthly-habits)
      - [5. List Habits by Category](#5-list-by-category)
      - [5. Return to Main Menu](#5-return-to-main-menu)

  * [Analytics Module](#analytics-mod)
      - [1. List All Habit's Streaks](#1-list-all-habit-s-streaks)
      - [2. List Longest Streak of Specific Habit](#2-list-longest-streak-of-specific-habit)
      - [3. List Streak Log of Specific Habit](#3-list-streak-log-of-specific-habit)
      - [4. Return to Main Menu](#4-return-to-main-menu-1)

  * [End Program](#end-programm)

# Habit Tracker
An Application for Tracking Habits - A Task of the IU Akademie. A Habit is something you do in a certain periodicity, like playing Soccer once a week or doing a monthly inventory. This Application helps you keeping track of all the things you want to pay attention to.
You can manage you habits by marking them as complete, by creating new ones, remove those you no longer do. It lets you check all your stored habits and shows you how well you are keeping a streak in your habits.


## Habit Tracker's Main Functions
The main options of this tracker are:

* Addition or Removal of Habits and Category
* Completing Habit
* Change the Periodicity of a Habit
* Listing the Habits (with filter choices)

### Streak Tracker
The Analytics Module lets you
* List the current streaks of all habits
* List the longest streak of specific habit
* List the streak log of specific habit



# Preparations
**Important**: This app was made with Python 3.12.0 so make sure it is installed on your OS. Latest version of Python is avaible at [https://www.python.org/downloads/](https://www.python.org/downloads/)

## Dependencies
* Python 3.12 +
* Questionary 2.0.1 +
* Rich 13.7.1

## Installing
Get the latest version of Python is avaible at [https://www.python.org/downloads/](https://www.python.org/downloads/) and be sure to check "ADD to path" in the Python installer. <br>

<br> Once the latest Python is installed, you need to install the necessary libraries. <br>

<br>*Questionary* - Questionary is a Python library for building pretty command line interfaces. 
<br>*Rich* - Rich is a Python library for rich text and beautiful formatting in the terminal.

<br>It gets installed by running the below command. Just type the name without the < > <br>
```
pip install <name>
```

### Packages for Test
To run the tests, the following libraries are needed. Use the same command listed in the prior section

<br>*Pytest* - Pytest is a Python testing framework that originated from the PyPy project. It can be used to write various types of software tests, including unit tests, integration tests, end-to-end tests, and functional tests. Its features include parametrized testing, fixtures, and assert re-writing. 
<br>*Freezegun* - FreezeGun is a library that allows your python tests to travel through time by mocking the datetime module.

## Start Program
After installing the dependencies and having downloaded the files from this repository, with those being saved in a separate folder. Open your command/terminal window and [cd](https://www.alphr.com/change-directory-in-cmd/) to your downloaded folder. Once that is complete, you can run the programm with:
```
python3 habit_tracker.py
```

You will be promted with a Command Line Interface where you can choose the desired action with the arrow keys and your keyboard.

```
Welcome to the Habit Tracker

================ MAIN = MENU =================
Make your Choice (Use arrow keys)
 » Addition or Removal
   Complete Habit
   Change the Periodicity of a Habit
   Listing Habits
   Analytics Module
   End Program
```

## Running Tests
To Run the Test, open your command/terminal window and [cd](https://www.alphr.com/change-directory-in-cmd/) to your the folder you stored the habit tracker in. Then run:
```
pytest
```



# Usage
**FYI**: You can delete the **HT.db** file with pre-defined demo habits [Namely: Swim, Tennis, Tea, Meeting and Study] or the **HT_weeks.db** file with test data of around 35 days. To swap the used database file, you alter the datanase default value in both habit_class.py's init and Habit_Tracker_Database.py's connect_database<br>


## Addition or Removal
#### 1. Add Habit
Upon running a new, blank version of the program with the **HT.db** file removed. Your first action should be adding a new habit. To do so, you choose the first option from the main menu:
```
 Addition or Removal
```
You will get a new sub-menu:
```
=== ADDITION OR REMOVAL MENU ===
Make your Choice (Use arrow keys)
 » Add a Habit
   Remove a Habit
   Delete a Category
```
You then get a promt to enter the necessary information for the habit, namely it's name, it's periodicity and it's category. For the category you will get the option to use an exsiting category or a new one.

#### 2. Remove Habit
With this selection, a list of all stored habits will be display and you can easily navigate with the arrow keys to select the one you want to delete and press enter.

#### 3. Delete Category
Like with the removal of a habit, a list with all categories is being displayed. Proceed as in remove habit.

#### 4. Return to Main Menu
Lets you return to the main menu.

## Complete Habit
With this Option, a list of all habits is being displayed and the user can choose with the arrow keys and enter which habit shell be marked as completed. 
<br>**FYI** There are functions in place, that prevent the user from completing a habit more than once in its periodicity. If the user fails to complete a habit intime, the streak will be reset to 0 before starting a new streak.

## Change Periodicity
In the event that the user wants to alter the periodicity of a existing habits, he may choose this option. e.g. going from doing a sports activity once a monthly to every week.
The list of all habits is going to be displayed and like before, the user can choose with the arrow keys to specific habit and then can choose from the avaiable periodicitys.


## Listing Habits
In this submenu the user may select filters for listing the stored habits.

#### 1. List ALL Habits
This Option will display every habit with their information (Habit Name, Periodicity, Category and Creation Time) in an aesthetic looking table (thanks to the rich libary)

#### 2. List Daily Habits
This Option puts the filter to only habits with periodicity of daily. Output like above.
#### 3. List Weekly Habits
This Option puts the filter to only habits with periodicity of weekly. Output like above.
#### 4. List Monthly Habits
This Option puts the filter to only habits with periodicity of monthly. Output like above.
#### 5. List by Category
This Option will display all available categories to choose from, the selected category will be the filter for the habit's display. Output like above.
#### 6. Return to Main Menu
Lets you return to the main menu.


## Analytics Module
In this submenu the user may his options for viewing habit's streaks.

#### 1. List All Habit's Streaks
This will display all stored habits and their current streak in an aesthetic looking table (thanks to the rich libary)

#### 2. View Longest Streak of Specific Habit
This will display a list of stored habits to choose from. It then will display the selected habit's longest streak and the last time it was completed. Output like above.

#### 3. View Streak Log of Specific Habit
This will display a list of stored habits to choose from. It then will display the selected habit's streak history. Output like above.

#### 4. Return to Main Menu
Lets you return to the main menu.

## End Program
Will close the application and return to the terminal.
