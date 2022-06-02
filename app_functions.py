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
                'Create a New Category', 'Edit a Category', 'Delete a Category', 'View a Category', 'Exit App']
    for item in menuItems:
        print ('{}.'.format(count),item)
        count += 1
    
    input1 = input('\nInput (1-10): ')
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
        for taskId1 in cursor:                                                  # If taskId already exists in tasks,  ### I would like to note this is **extremely** unlikely to happen. But it's always good to make sure!
            if taskId not in taskId1:                                           # Generate another one, else print and return
                print("\nTask ID:",taskId)                                      
                return "'"+taskId+"'"

def inputTask():                                                                # Function for asking user input for their task description
    while(1):                                                                   # Infinite loop
        try:
            task = input("\nAdd task description: ")                            # User input
            if len(task) > 30:                                                  # If task description is longer than 30 characters, ask for input again.
                print('Task cannot be longer than 30 characters. Try again.')
            elif "'" in task or '"' in task:
                print("The characters ' and",'" cannot be used.')
            else:
                return "'"+task+"'"                                             # Else return it
        except:
            print('An error has occurred with your input. Please try again.')

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

def inputCategory(cursor):                                                              # Function to ask user input for category name
    while(1):
        categoryName = ''                                                                           # Infinite loop
        while categoryName == '' or len(categoryName) > 20 or "'" in categoryName or '"' in categoryName:
            categoryName = input("\nWhat category is your task in? Input: ")
            if categoryName == '': print('Category cannot be empty!')
            elif len(categoryName) > 20: print('Category name is too long!')
            elif "'" in categoryName or '"' in categoryName: print("The characters ' and",'" cannot be used.')

        try:
            cursor.execute('SELECT categoryname FROM category')
            for category in cursor:                                                 # If category exists,
                if categoryName in category:                                        # return category name
                    return "'"+categoryName+"'"
                                                                                    # Else create new category with input name 
            input1 = input('Category does not exist! Do you want to create a new "'+categoryName+'" category?\nInput (Y/N): ')   
            if input1 == 'Y' or input1 == 'y':
                categoryName = "'"+categoryName+"'"
                dateCreated = 'CURDATE()'
                cursor.execute('INSERT INTO category VALUES ('+categoryName+', '+dateCreated+')')
                return categoryName   
            elif input1 == 'N' or input1 == 'n':
                break
            else:
                print('Invalid input!')
        except mariadb.Error:
            print('An error has occurred with your input! Please try again.')                                                           

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

def inputCategoryName(cursor):
    while(1):                                                                   # Infinite loop
        categoryName = input("\nEnter category name: ")
        cursor.execute('SELECT categoryname FROM category')
        exists = False
        for category in cursor:                                                 # If category exists,
            if categoryName in category:  
                exists = True
                break         
        
        if exists:
            print("Category already exists!")   
        else:
            return "'"+categoryName+"'"                      

def addCategory(cursor):                                                            # Function for adding a category to the database
    categoryName = inputCategoryName(cursor)
    dateCreated = 'CURDATE()'

    clearTerminal()

    statement = "INSERT INTO category VALUES ("+categoryName+", "+dateCreated+")"
    print("Executed", statement+";")
    return cursor.execute(statement)

def deleteCategory(cursor):
    clearTerminal()
    while(1):
        exists = False
        delete = input('\nEnter category name to be deleted: ')

        cursor.execute('SELECT * from category')
        for category in cursor:
            if delete in category:
                exists = True
                break
            else:
                exists = False

        if not exists:
            print("Category name does not exist!")
            break
        else:
            clearTerminal()
            statement = "DELETE FROM task WHERE categoryname='"+delete+"'"
            cursor.execute(statement)
            statement = "DELETE FROM category WHERE categoryname = '"+delete+"'"
            print("Executed", statement+";")
            return cursor.execute(statement)

def viewCategory(cursor):
    clearTerminal()
    print('CATEGORY:\n')
    cursor.execute('SELECT * from category')
    for category in cursor:
        print('Category Name:',category[0])
        print('Date Created:',category[1],end='\n-------------------------\n')
    
    while(1):
        input1 = input('\nDo you want to view tasks in a specific category? (Y/N): ')

        if input1 == 'Y' or input1 == 'y':
            category = input('Input category name: ')
            cursor.execute('SELECT * from task WHERE categoryname="'+category+'"')

            clearTerminal()

            if len(cursor.fetchall()) == 0:
                print('Category does not exist.')
                break

            cursor.execute('SELECT * from task WHERE categoryname="'+category+'"')
            print('\nTASKS:\n')
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
            break

        if input1 == 'N' or input1 == 'n':
            break
        
        else:
            print('Invalid input!')