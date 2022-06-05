import os
import random
import mysql.connector as mariadb
from datetime import datetime
from datetime import timedelta

sep = '\n-------------------------\n'

def clearTerminal():  # Clear the terminal.
    os.system('cls' if os.name == 'nt' else 'clear')

def databaseLogin():  # Function for logging in to MariaDB
    password = input('Enter Password: ') # Get user input for MariaDB root password.

    try:
        mariadb_connection = mariadb.connect(user='cmsc127_PJAI', password=password, database='app_data', host='localhost', port='3306')
    except mariadb.Error as err:
        if err.errno == 1045:
            print("\nIncorrect password.\n")
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
        print ('[{}]'.format(count),item)
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
                print("\nInput your category name again.",end="")
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
        print('Category:',task[7],end=sep)

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

def addCategory(cursor):
                                                                # Function for adding a category to the database
    while(1):
        try:
            categoryName = inputCategoryName(cursor)
            dateCreated = 'CURDATE()'

            if len(categoryName) > 20:
                print("Category name cannot be longer than 20 characters. Please try again.")
            else:
                clearTerminal()
                statement = "INSERT INTO category VALUES ("+categoryName+", "+dateCreated+")"
                print("Executed", statement+";")
                return cursor.execute(statement)
        except:
            print("An error has occurred. Please try again.")

def deleteCategory(cursor):
    clearTerminal()
    print('CATEGORY:\n')
    cursor.execute('SELECT * from category')
    for category in cursor:
        print('Category Name:',category[0])
        print('Date Created:',category[1],end=sep)

    while(1):
        exists = False
        delete = input('Enter category name to be deleted: ')

        cursor.execute('SELECT categoryname from category')
        for category in cursor:
            if delete in category:
                exists = True
                break
            else:
                exists = False

        if not exists:
            print("Category name does not exist!")
            return 0
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
        print('Date Created:',category[1],end=sep)
    
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
                print('Category:',task[7],end=sep)
            break

        if input1 == 'N' or input1 == 'n':
            break
        
        else:
            print('Invalid input!')

def editCategory(cursor, mariadb):
    
    clearTerminal()
    print('CATEGORY:\n')
    cursor.execute('SELECT * from category')
    for category in cursor:
        print('Category Name:',category[0])
        print('Date Created:',category[1],end=sep)

    while(1):
        print("\nEnter the name of the category you want to edit.")
        category_name = input("Category: ")
        exists = False
        cursor.execute("SELECT categoryname FROM category")
        for category in cursor:
            if category_name in category:
                exists = True
                break
        
        if exists:
            try:
                new_category_name = input("Enter new category name: ")

                cursor.execute("SELECT categoryname FROM category")
                for category in cursor:
                    if new_category_name in category:
                        clearTerminal()
                        print("\nYou are attempting to edit a category and change its name to an already existing category. You cannot do this.")
                        return

                if len(new_category_name) > 20:
                    print("Category name cannot be longer than 20 characters.")
                
                else:
                    cursor.execute("SELECT dateCreated FROM category WHERE categoryname='"+category_name+"'")
                    dateCreated = cursor.fetchone()[0]
                    year = str(dateCreated.year)
                    month = str(dateCreated.month)
                    day = str(dateCreated.day)

                    cursor.execute("UPDATE task SET categoryname=NULL WHERE categoryname='"+category_name+"'")
                    cursor.execute("INSERT INTO category VALUES ('"+new_category_name+"', STR_TO_DATE('"+year+","+month+","+day+"','%Y,%m,%d'))")
                    cursor.execute("UPDATE task SET categoryname='"+new_category_name+"' WHERE categoryname IS NULL")
                    cursor.execute("DELETE FROM category WHERE categoryname='"+category_name+"'")
                    
                    clearTerminal()
                    print("Executed successfully!")
                    return
            except mariadb.Error:
                print('An error occurred. Please try again.')
        else:
            print("That category name doesn't exist!")
            input1 = input("Do you still want to continue? (Y/N): ")
            if input1 == 'n' or input1 == 'N':
                return 0
            elif input1 == 'y' or input1 == 'Y':
                continue
            else:
                print("Invalid input!")
                return 0

def inputDateStarted():                                                 #used in editTask()
    format = "%Y-%m-%d"                                                 #edits the task's date started
    while(1):                                                                   
        dateStarted = input("\nDate Started (Leave blank if none, format is yyyy-mm-dd): ")

        if dateStarted == '':                                                      
            dateStarted = 'NULL'.strip(' ')                                       
            return dateStarted
        else:                                                                   
            try:                                                                
                res = bool(datetime.strptime(dateStarted, format))
            except ValueError:
                res = False

            if not res:                                                         
                print('Invalid date format!\n')
            else:                                                               
                return "'"+dateStarted+"'"

def inputDateFinished():                                                #used in editTask()
    format = "%Y-%m-%d"                                                 #edits the task's date started
    while(1):                                                                   
        dateFinished = input("\nDate Finished: (Leave blank if none, format is yyyy-mm-dd): ")

        if dateFinished == '':                                                      
            dateFinished = 'NULL'.strip(' ')                                        
            return dateFinished
        else:                                                                   
            try:                                                                
                res = bool(datetime.strptime(dateFinished, format))
            except ValueError:
                res = False

            if not res:                                                        
                print('Invalid date format!\n')
            else:                                                               
                return "'"+dateFinished+"'"

def deleteTask(cursor):
    clearTerminal()
    
    cursor.execute('SELECT * FROM task')                             #displays some of the details of the tasks
    for task in cursor:
        print('Task ID:',task[0])
        print('Description:',task[1])
        print('Category:',task[7],end=sep)

    while(1):
        print("Enter the task ID of the task you want to be deleted.\n")
        taskID = input("Task ID: ")
        exists = False
        
        cursor.execute('SELECT taskid FROM task')                        #looks for the entered task id
        for task in cursor:
            if taskID in task:
                exists = True
                break

        if exists == True:                                          #if the entered task id exists, delete
            clearTerminal()
            statement = "DELETE FROM task WHERE taskid = '"+taskID+"'"
            print("Executed", statement+";")
            print("Task has been succesfully deleted!")
            return cursor.execute(statement)
        else:
            print("Task ID doesn't exist!")
            input1 = input("Do you still want to continue? (Y/N): ")
            if input1 == 'n' or input1 == 'N':
                return 0
            elif input1 == 'y' or input1 == 'Y':
                continue
            else:
                print("Invalid input!")
                return 0


def markTask(cursor):
    clearTerminal()
    
    cursor.execute("SELECT * FROM task")
    for task in cursor:
        print('Task ID:',task[0])
        print('Description:',task[1])
        print('Date Finished:',task[4])
        if task[6] == 0:
            print('Status: Not finished')
        else:
            print('Status: Finished')
        print('Category:',task[7],end=sep)

    while(1):
        print("Enter the task ID of the task you want to be marked as DONE.")
        taskID = input("\nTask ID: ")
        exists = False
        
        cursor.execute('SELECT taskid FROM task')                        #looks for the task id
        for task in cursor:
            if taskID in task:
                exists = True
                break

        if exists == True:                                          #if the task id exists, then update the status of the task to DONE
            clearTerminal()
            statement = "UPDATE task SET taskstatus=1 WHERE taskid = '"+taskID+"'"
            print("Executed", statement+";")
            print("Task has been successfully marked as DONE!")
            return cursor.execute(statement)

        else:
            print("Task ID doesn't exist!")
            input1 = input("Do you still want to continue? (Y/N): ")
            if input1 == 'n' or input1 == 'N':
                return 0
            elif input1 == 'y' or input1 == 'Y':
                continue
            else:
                print("Invalid input!")
                return 0
    

def editTask(cursor):           
    clearTerminal()
    menuItems = ['Description', 'Date Started', 'Date Finished', 'Deadline', 'Status', 'Category', 'Cancel']
    
    viewTasks(cursor)
    print("Enter the Task ID of the task you want to edit.")
    taskId = input("Input: ")
    exists = False
    
    cursor.execute('SELECT taskid FROM task')                        #looks for the task id
    for task in cursor:     
        if taskId in task and taskId != '':
            exists = True
            break

    if exists:                                                  #if the task id exists, print the options
        clearTerminal()
        while(1):
            print("Which content of the task do you want to edit?")
            count = 1
            for item in menuItems:
                print ('[{}]'.format(count),item)
                count += 1

            choice = input("Enter choice (1-6): ")
            statement = ''
            if choice == '1':                                       #edit the task description
                new_description = inputTask()
                statement = "UPDATE task SET taskdescription="+new_description+" WHERE taskid = '"+taskId+"'" 
            
            elif choice == '2':                                     #edit the date started
                new_date_started = inputDateStarted()
                statement = "UPDATE task SET datestarted="+new_date_started+" WHERE taskid = '"+taskId+"'"    
            
            elif choice == '3':                                     #edit the date finished
                new_date_finished = inputDateFinished()
                statement = "UPDATE task SET datefinished="+new_date_finished+" WHERE taskid = '"+taskId+"'"   

            elif choice == '4':                                     #edit the deadline
                new_deadline = inputDeadline()
                statement = "UPDATE task SET deadline="+new_deadline+" WHERE taskid = '"+taskId+"'"      
            
            elif choice == '5':                                     #edit status                
                print("\nPlease choose from the following:")
                print("[1] Finished")
                print("[2] Not Yet Finished")
                
                input_status = input("Enter status (1-2): ")

                if input_status == '1':
                    statement = "UPDATE task SET taskstatus=1 WHERE taskid = '"+taskId+"'"     
                elif input_status == '2':
                    statement = "UPDATE task SET taskstatus=0 WHERE taskid = '"+taskId+"'"    
                else:
                    clearTerminal()
                    print("Invalid status! Please try again.")
            
            elif choice == '6':                                     #edit category     
                newCategory = inputCategory(cursor)
                statement = "UPDATE task SET categoryname="+newCategory+" WHERE taskid = '"+taskId+"'"

            elif choice == '7':
                clearTerminal()
                break
            else:
                clearTerminal()
                print("Invalid choice!\n")
            
            if statement != '':
                clearTerminal()
                print(menuItems[int(choice)-1],'has been updated!')
                try:
                    print("Executed", statement+";")
                    return cursor.execute(statement)
                except mariadb.Error:
                    print('An error occurred! Try again.')
                    break
    else:
        print("Task ID doesn't exist!")