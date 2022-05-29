import mysql.connector as mariadb
import app_functions as app

#=============================================#
#Function to execute SQL queries
def runSql(file):
    database = open(file, 'r')
    databaseLines = database.read()
    database.close()
    line = databaseLines.split(';')

    for x in line:
        cursor.execute(x)
#=============================================#

app.clearTerminal()

password = input('\nEnter MariaDB root password: ') # Get user input for MariaDB root password.

try:
    mariadb_connection = mariadb.connect(user='root', password=password, host='localhost', port='3306')
except mariadb.Error as err:
    if err.errno == 1698:
        print("\nIncorrect root password.\n")
        exit()
    else:
        print(err)
        exit()

cursor = mariadb_connection.cursor()

filename = 'data.sql'
runSql(filename)
cursor.close()
print('\nDatabase has been sourced from', filename, 'file\nYou may now run the main app.\n')