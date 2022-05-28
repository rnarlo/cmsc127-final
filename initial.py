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

cursor = app.databaseLogin()

filename = 'data.sql'
runSql(filename)
cursor.close()
print('\nDatabase has been sourced from', filename, 'file\nYou may now run the main app.\n')