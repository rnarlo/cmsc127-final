import os
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

    return mariadb_connection.cursor()
