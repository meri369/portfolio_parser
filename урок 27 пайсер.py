import sqlite3
from sqlite3 import Error

def sql_connection(): # устанавливает конект
    try:
        con = sqlite3.connect("mydatabase.db")
        return con
    except Error: # если есть ошибка то ерор(перехват ошибки )
        print(Error)

def sql_table(con): #execute-создает таблицу
    cursorOBJ = con.cursor()
    cursorOBJ.execute(
        "CREATE TABLE employees(id integer PRIMARY KEY, name text, salary real, department text, position text, hireDate text)")

    con.commit()

con=sql_connection() #сохраняет сделанные изменения
sql_table(con) #вызов обеих функция 