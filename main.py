import mysql.connector as mariadb
import app_functions as app

app.clearTerminal()
mariadb_connection = app.databaseLogin()
cursor = mariadb_connection.cursor(buffered=True)
app.clearTerminal()

sep = '========================='

print(sep*2)
print('Hello! Welcome to your task-listing application!')
print(sep*2)

while(1):
    input1 = app.printMenu()
    
    if input1 == '1':
        app.addTask(cursor)
        mariadb_connection.commit()
    elif input1 == '11':
        cursor.close()
        print('\nHave a good day!\n')
        exit()
    else:
        print('\nInvalid input!')
    
