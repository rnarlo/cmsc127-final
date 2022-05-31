import os
import random
import mysql.connector as mariadb
from datetime import datetime
from datetime import timedelta

def clearTerminal():  # Clear the terminal.
    os.system('cls' if os.name == 'nt' else 'clear')

def databaseLogin():  # Function for logging in to MariaDB
    password = input('Enter MariaDB root password: ') # Get user input for MariaDB root password.

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

def printMenu():    # Function for printing main menu where the user can choose what to do
    print()
    count = 1
    menuItems = ['Create a New Task', 'Edit an Existing Task', 'Delete a Task', 'View All Tasks', 'Mark a Task As Done', 
                'Create a New Category', 'Edit a Category', 'Delete a Category', 'View a Category', 'Add a Task To Category', 'Exit App']
    for item in menuItems:
        print ('{}. '.format(count),item)
        count += 1
    
    input1 = input('\nInput (1-11): ')
    return input1

def generateTaskId(cursor):                                                     # Function for generating a unique task ID that's 10 characters long
    while(1):                                                                   # Infinite loop
        taskId = ''
        for i in range(10):
            integer = random.randint(0, 9)                                      # Generates a random integer from 0-9
            taskId += (str(integer))                                            # Adds them together in one string
            
        cursor.execute('SELECT taskid FROM task')  
        if len(cursor.fetchall()) == 0:                                         # If there are no tasks,
            print("\nTask ID:",taskId)                                          # print and return taskId
            return "'"+taskId+"'"

        cursor.execute('SELECT taskid FROM task')      
        for taskId1 in cursor:                                                  # If taskId already exists in tasks,
            if taskId not in taskId1:                                           # Generate another one, else print and return
                print("\nTask ID:",taskId)
                return "'"+taskId+"'"

def inputTask():                                                                # Function for asking user input for their task description
    while(1):                                                                   # Infinite loop
        task = input("\nAdd task description: ")                                # User input
        if len(task) > 30:                                                      # If task description is longer than 30 characters, ask for input again.
            print('Task cannot be longer than 30 characters. Try again.')
        else:
            return "'"+task+"'"                                                 # Else return it

def inputDeadline():                                                            # Function for asking user input for task deadline
    format = "%Y-%m-%d"                                                         # Date format is yyyy-mm-dd
    yesterday = datetime.now() - timedelta(days = 1)                            # Date yesterday
    while(1):                                                                   
        deadline = input("\nAdd deadline (Leave blank if none, format is yyyy-mm-dd): ")

        if deadline == '':                                                      # If there is no input,
            deadline = 'NULL'.strip(' ')                                        # assume task has no deadline and return string 'NULL'
            return deadline
        else:                                                                   # Else
            try:                                                                # Check if input string follows correct format
                res = bool(datetime.strptime(deadline, format))
            except ValueError:
                res = False

            if not res:                                                         # If format is incorrect, ask for input again.
                print('Invalid date format!')
            else:                                                               # Else check if date is in the past. If it is, ask for input again.
                if datetime.strptime(deadline,format) < yesterday:
                    print('Date cannot be in the past!')
                else:                                                           # Else return the provided deadline
                    return "'"+deadline+"'"

def inputWillStart():                                                           # Function to ask user if the task will be started today
    while(1):
        willStart = input("\nAre you going to start working on the task today? (Y/N): ")
        if willStart == 'Y' or willStart == 'y':                                # If yes,
            dateStarted = 'CURDATE()'                                           # dateStarted will be today
            return dateStarted
        elif willStart == 'N' or willStart == 'n':                              # Else,
            dateStarted = 'NULL'.strip(' ')                                     # assume dateStarted will be in the future and return string 'NULL'
            return dateStarted
        else:
            print('Invalid input! Try again.')                                  # If input is invalid, ask for input again

def inputCategory(cursor):                                                      # Function to ask user input for category name
    while(1):                                                                   # Infinite loop
        categoryName = input("\nWhat category is your task in? Input: ")
        cursor.execute('SELECT categoryname FROM category')

        for category in cursor:                                                 # If category exists,
            if categoryName in category:                                        # return category name
                return "'"+categoryName+"'"

        print('Category does not exist!')                                       # Else ask for input again 
                                                                                # TODO: Ask user if they want to create said category that does not exist

def addTask(cursor):                                                            # Function for adding a task to the database
    clearTerminal()

    taskId = generateTaskId(cursor)
    task = inputTask()
    dateToday = 'CURDATE()'
    dateStarted = inputWillStart()
    deadline = inputDeadline()
    categoryName = inputCategory(cursor)

    clearTerminal()

    statement = "INSERT INTO task VALUES ("+taskId+", "+task+", "+dateToday+", "+dateStarted+", "+"NULL, "+deadline+", "+"0, "+categoryName+")"
    print("Executed", statement+";")
    return cursor.execute(statement)

def viewTasks(cursor):
    clearTerminal()
    print('TASKS:\n')
    cursor.execute('SELECT * from task')
    for task in cursor:
        print('Task ID:',task[0])
        print('Description:',task[1])
        print('Date Added:',task[2])
        print('Date Started:',task[3])
        print('Date Finished:',task[4])
        print('Deadline:',task[5])
        if task[6] == 0:
            print('Status: Not finished')
        else:
            print('Status: Finished')
        print('Category:',task[7],end='\n-------------------------\n')
