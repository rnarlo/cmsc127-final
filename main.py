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

cursor.execute('SELECT * from task')
for task in cursor:
    task_counter += 1

cursor.execute('SELECT * from category')
for category in cursor:
    category_counter += 1


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
            app.clearTerminal()
            print("There are no tasks in the list yet!")
    elif input1 == '3':                         #Delete a Task
        if task_counter > 0:                         
            delete = app.deleteTask(cursor)    
            if delete == 0:
                continue  
            else:
                mariadb_connection.commit()
                task_counter -= 1
        else:
            app.clearTerminal()
            print("There are no tasks in the list yet!") 
    elif input1 == '4':                         #View all Tasks
        app.viewTasks(cursor)
        input1 = input('\nIf you are done viewing your tasks, press Enter.\n')
        app.clearTerminal()
    elif input1 == '5':                         #Mark Task as Done
        if task_counter > 0:                          
            delete = app.markTask(cursor)
            if delete == 0:
                continue  
            else:
                mariadb_connection.commit()
        else:
            app.clearTerminal()
            print("There are no tasks in the list yet!")
    elif input1 == '6':                         #Create a New Category
        app.clearTerminal()
        app.addCategory(cursor)
        mariadb_connection.commit()
        category_counter+=1
    elif input1 == '7':
        if category_counter>0:
            app.clearTerminal()
            delete = app.editCategory(cursor)
            if delete == 0:
                continue  
            else:
                mariadb_connection.commit()
        else:
            app.clearTerminal()
            print("There are no categories in the list yet!")
    elif input1 == '8':                         #Delete a Category
        if category_counter>0:                         
            delete = app.deleteCategory(cursor)
            if delete == 0:
                continue  
            else:
                mariadb_connection.commit()
                category_counter-=1
        else:
            app.clearTerminal()
            print("There are no categories in the list yet!")
    elif input1 == '9':                         #View a Category
        if category_counter>0:
            app.viewCategory(cursor) 
            input1 = input('\nIf you are done viewing, press Enter.\n')
            app.clearTerminal()
        else:
            app.clearTerminal()
            print("There are no categories in the list yet!")
    elif input1 == '10':
        cursor.close()                          #Exit App
        print('\nHave a good day!\n')
        exit()
    else:
        print('\nInvalid input!')
    
