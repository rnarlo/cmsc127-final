import mysql.connector as mariadb
import app_functions as app

app.clearTerminal()
cursor = app.databaseLogin()
app.clearTerminal()

sep = '========================='

print(sep*2)
print("Hello! Welcome to your task-listing application!")
print(sep*2)

while(1):
    print('\nWhat do you want to do?\n')
    print('1. Create a New Task')
    print('2. Edit an Existing Task')
    print('3. Delete a Task')
    print('11. Exit app')
    input1 = input('\nInput: ')

    if input1 == '11':
        print("\nHave a good day!\n")
        exit()
