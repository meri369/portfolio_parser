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
    cursorOBJ.execute("INSERT INTO employees VALUES(1, 'John', 700, 'HR', 'Manager', '2017-01-04')")

    con.commit()

con=sql_connection() #сохраняет сделанные изменения
sql_table(con) #вызов обеих функция