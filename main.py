from unicodedata import category
import app_functions as app

app.clearTerminal()
mariadb_connection = app.databaseLogin()
cursor = mariadb_connection.cursor(buffered=True)
app.clearTerminal()

sep = '========================='

print(sep*2)
print('Hello! Welcome to your task-listing application!')
print(sep*2)

task_counter = 0
category_counter = 0

while(1):
    input1 = app.printMenu()
    
    if input1 == '1':                           #Create a New Task
        app.addTask(cursor)
        mariadb_connection.commit()
        task_counter += 1
    elif input1 == '2':                         #Edit an Existing Task
        if task_counter > 0:                         
            app.editTask(cursor)
            mariadb_connection.commit()
        else:
            print("There's no task in the task list yet!")
    elif input1 == '3':                         #Delete a Task
        if task_counter > 0:                         
            app.deleteTask(cursor)                  
            mariadb_connection.commit()
            task_counter -= 1
        else:
            print("There's no task in the list yet!") 
    elif input1 == '4':                         #View all Tasks
        app.viewTasks(cursor)
        input1 = input('\nIf you are done viewing your tasks, press Enter.\n')
        app.clearTerminal()
    elif input1 == '5':                         #Mark Task as Done
        if task_counter > 0:                          
            app.markTask(cursor)
            mariadb_connection.commit()
        else:
            print("There's no task in the list yet!")
    elif input1 == '6':                         #Create a New Category
        app.clearTerminal()
        app.addCategory(cursor)
        mariadb_connection.commit()
        category_counter+=1
    elif input1 == '8':                         #Delete a Category
        if category_counter>0:                         
            app.deleteCategory(cursor)
            mariadb_connection.commit()
            category_counter-=1
        else:
            print("There's no category in the list yet!")
    elif input1 == '9':                         #View a Category
        app.viewCategory(cursor) 
        input1 = input('\nIf you are done viewing, press Enter.\n')
        app.clearTerminal()
    elif input1 == '10':
        cursor.close()                          #Exit App
        print('\nHave a good day!\n')
        exit()
    else:
        print('\nInvalid input!')
    
