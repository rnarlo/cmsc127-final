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

password = input('Enter MariaDB root password: ') # Get user input for MariaDB root password.

try:
    mariadb_connection = mariadb.connect(user='root', password=password, host='localhost', port='3306')
except mariadb.Error as err:
    if err.errno == 1698:
        print("\nIncorrect root password.\n")
        exit()
    else:
        print(err)
        exit()

cursor = mariadb_connection.cursor(buffered=True)

cursor.execute('SHOW DATABASES')

for database in cursor:
    if 'app_data' in database:
        print("\nThe 'app_data' database has already been initialized. Doing so again will wipe all of the data in it. Continue? (Y/N)")
        input1 = input('Input: ')

        if input1 == 'N' or input1 == 'n':
            exit()
        if input1 == 'Y' or input1 == 'y':
            break
        else:
            print('\nInvalid input!\n')
            exit()

filename = 'data.sql'
runSql(filename)
mariadb_connection.commit()
cursor.close()
print('\nDatabase has been sourced from', filename, 'file\nYou may now run the main app.\n')
