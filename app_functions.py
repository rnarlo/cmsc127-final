import os
import random
import mysql.connector as mariadb

def clearTerminal():  # Clear the terminal.
    os.system('cls' if os.name == 'nt' else 'clear')

def databaseLogin():
    password = input('\nEnter MariaDB root password: ') # Get user input for MariaDB root password.

    try:
        mariadb_connection = mariadb.connect(user='root', password=password, database='app_data', host='localhost', port='3306')
    except mariadb.Error as err:
        if err.errno == 1698:
            print("\nIncorrect root password.\n")
            exit()
        else:
            print(err)
            exit()

    return mariadb_connection

def printMenu():
    print()
    count = 1
    menuItems = ['Create a New Task', 'Edit an Existing Task', 'Delete a Task', 'View All Tasks', 'Mark a Task As Done', 
                'Create a New Category', 'Edit a Category', 'Delete a Category', 'View a Category', 'Add a Task To Category', 'Exit App']
    for item in menuItems:
        print ('{}. '.format(count),item)
        count += 1
    
    input1 = input('\nInput (1-11): ')
    return input1

def addTask(cursor):
    taskId = ''
    for i in range(10):
        integer = random.randint(0, 9)
        taskId += (str(integer))    # Keep appending random characters using chr(x)

    taskId = "'"+taskId+"'"
    print("Task ID:",taskId)
    task = "'"+input("\nAdd task description: ")+"'"
    deadline = input("\nAdd deadline (Leave blank if none, format is yyyy-mm-dd): ")
    willStart = input("\nAre you going to start working on the task today? (Y/N): ")
    categoryName = "'"+input("\nWhat category is your task in? Input: ")+"'"

    dateToday = 'CURDATE()'

    if willStart == 'Y' or willStart == 'y':
        dateStarted = dateToday
    else:
        dateStarted = 'NULL'

    if deadline == '':
        deadline = 'NULL'
    else:
        deadline = "'"+deadline+"'"

    statement = "INSERT INTO task VALUES ("+taskId+", "+task+", "+dateToday+", "+dateStarted+", "+"NULL, "+deadline+", "+"0, "+categoryName+")"
    print("\nExecuted", statement)
    return cursor.execute(statement)

