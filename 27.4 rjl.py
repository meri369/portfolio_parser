import sqlite3

con = sqlite3.connect('mydatabase.db')

def sql_fetch(con):
   cursorObj = con.cursor()

   cursorObj.execute('SELECT id, name FROM employees WHERE salary > 100.0')

   rows = cursorObj.fetchall()

   for row in rows:
       print(row)


sql_fetch(con)