"""Урок 34.1. Хранение данных
1. Хранение данных
Давайте создадим новую базу данных и поработаем с ней
"""


import sqlite3
from sqlite3 import Error


def sql_connection():
    try:

        con = sqlite3.connect(':memory:')

        print("Connection is established: Database is created in memory")

    except Error:

        print(Error)

    finally:

        con.close()


sql_connection()


"""
Сначала импортируется модуль sqlite3, затем определяется функция с именем sql_connection.
 Внутри функции определен блок try, где метод connect() возвращает объект соединения после установления соединения.
Затем определен блок исключений, который в случае каких-либо исключений печатает сообщение об ошибке.
 Если ошибок нет, соединение будет установлено, тогда скрипт распечатает текст «Connection is established:
  Database is created in memory».
Далее производится закрытие соединения в блоке finally. Закрытие соединения необязательно,
 но это хорошая практика программирования, позволяющая освободить память от любых неиспользуемых ресурсов.
Чтобы создать таблицу в SQLite3, выполним запрос Create Table в методе execute().
 Для этого выполним следующую последовательность шагов:
Создание объекта подключения
Объект Cursor создается с использованием объекта подключения
Используя объект курсора, вызывается метод execute с запросом create table в качестве параметра.
Давайте создадим таблицу Employees со следующими колонками:
employees (id, name, salary, department, position, hireDate)"""

import sqlite3

from sqlite3 import Error


def sql_connection():
   try:

       con = sqlite3.connect('mydatabase.db')

       return con

   except Error:

       print(Error)


def sql_table(con):
   cursorObj = con.cursor()

   cursorObj.execute(
       "CREATE TABLE employees(id integer PRIMARY KEY, name text, salary real, department text, position text, hireDate text)")

   con.commit()


con = sql_connection()
sql_table(con)

"""
В приведенном выше коде определено две функции: первая устанавливает соединение;
 а вторая - используя объект курсора выполняет SQL оператор create table.
Метод commit() сохраняет все сделанные изменения. 
В конце скрипта производится вызов обеих функций.
Чтобы вставить данные в таблицу воспользуемся оператором INSERT INTO.
Рассмотрим следующую строку кода:
cursorObj.execute("INSERT INTO employees VALUES(1, 'John', 700, 'HR', 'Manager', '2017-01-04')")
Также можем передать значения / аргументы в оператор INSERT в методе execute ().
 Также можно использовать знак вопроса (?) в качестве заполнителя для каждого значения.
  Синтаксис INSERT будет выглядеть следующим образом:
cursorObj.execute('''INSERT INTO employees(id, name, salary, department, position, hireDate) VALUES(?, ?, ?, ?, ?, ?)''', entities)
Где кортеж entities содержат значения для заполнения одной строки в таблице:
entity = (2, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')

"""


import sqlite3

con = sqlite3.connect('mydatabase.db')


def sql_insert(con, entities):
   cursorObj = con.cursor()

   cursorObj.execute(
       'INSERT INTO employees(id, name, salary, department, position, hireDate) VALUES(?, ?, ?, ?, ?, ?)', entities)

   con.commit()


entities = (2, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')

sql_insert(con, entities)



"""Предположим, что нужно обновить имя сотрудника, чей идентификатор равен 2.
Для обновления будем использовать инструкцию UPDATE. 
Также воспользуемся предикатом WHERE в качестве условия для выбора нужного сотрудника."""


import sqlite3

con = sqlite3.connect('mydatabase.db')
def sql_update(con):
   cursorObj = con.cursor()
   cursorObj.execute('UPDATE employees SET name = "Rogers" where id = 2')
   con.commit()

sql_update(con)


"""Это изменит имя Эндрю на Роджерс.
Оператор SELECT используется для выборки данных из одной или более таблиц.
 Если нужно выбрать все столбцы данных из таблицы, можете использовать звездочку (*).
SQL синтаксис для этого будет следующим:
select * from table_name

В SQLite3 инструкция SELECT выполняется в методе execute объекта курсора.
 Например, выберем все стрoки и столбцы таблицы employee:
cursorObj.execute('SELECT * FROM employees ')

Если нужно выбрать несколько столбцов из таблицы, укажем их, как показано ниже:
select column1, column2 from tables_name

Например,
cursorObj.execute('SELECT id, name FROM employees')

Оператор SELECT выбирает все данные из таблицы employees БД.

Чтобы извлечь данные из БД выполним инструкцию SELECT,
 а затем воспользуемся методом fetchall() объекта курсора для сохранения значений в переменной.
При этом переменная будет являться списком, где каждая строка из БД будет отдельным элементом списка.
Далее будет выполняться перебор значений переменной и печатать значений.
"""


import sqlite3

con = sqlite3.connect('mydatabase.db')


def sql_fetch(con):
   cursorObj = con.cursor()

   cursorObj.execute('SELECT * FROM employees')

   rows = cursorObj.fetchall()

   for row in rows:
       print(row)


sql_fetch(con)

"""
Также можно использовать fetchall() в одну строку:
[print(row) for row in cursorObj.fetchall()]

Если нужно извлечь конкретные данные из БД, воспользуйтесь предикатом WHERE.
Например, выберем идентификаторы и имена тех сотрудников, чья зарплата превышает 800.
Для этого заполним нашу таблицу большим количеством строк, а затем выполним запрос.
Можете использовать оператор INSERT для заполнения данных или ввести их вручную в программе браузера БД.
Теперь, выберем имена и идентификаторы тех сотрудников, у кого зарплата больше 100:
"""


import sqlite3

con = sqlite3.connect('mydatabase.db')

def sql_fetch(con):
   cursorObj = con.cursor()

   cursorObj.execute('SELECT id, name FROM employees WHERE salary > 100.0') # выводим имя где зарплата больше 100

   rows = cursorObj.fetchall()

   for row in rows:
       print(row)


sql_fetch(con)


"""
В приведенном выше операторе SELECT вместо звездочки (*) были указаны атрибуты id и name.

Счетчик строк SQLite3 используется для возврата количества строк,
 которые были затронуты или выбраны последним выполненным запросом SQL.
Когда вызывается rowcount с оператором SELECT, будет возвращено -1,
 поскольку количество выбранных строк неизвестно до тех пор, пока все они не будут выбраны. Рассмотрим пример:
print(cursorObj.execute('SELECT * FROM employees').rowcount)

Поэтому, чтобы получить количество строк, нужно получить все данные, а затем получить длину результата:


rows = cursorObj.fetchall()

print(len(rows))

Когда оператор DELETE используется без каких-либо условий (предложение where),
все строки в таблице будут удалены, а общее количество удаленных строк будет возвращено rowcount.
print(cursorObj.execute('DELETE FROM employees').rowcount)

Если ни одна строка не удалена, будет возвращено 0.

Чтобы вывести список всех таблиц в базе данных SQLite3, нужно обратиться к таблице sqlite_master,
а затем использовать fetchall() для получения результатов из оператора SELECT.
Sqlite_master - это главная таблица в SQLite3, в которой хранятся все таблицы.
"""


import sqlite3

con = sqlite3.connect('mydatabase.db')


def sql_fetch(con):
   cursorObj = con.cursor()

   cursorObj.execute('SELECT name from sqlite_master where type= "table"')

   print(cursorObj.fetchall())


sql_fetch(con)

"""
При создании таблицы необходимо убедиться, что таблица еще не существует.
Аналогично, при удалении таблицы она должна существовать.
Чтобы проверить, если таблица еще не существует,
 используем «if not exists» с оператором CREATE TABLE следующим образом:

"""

import sqlite3
con = sqlite3.connect('mydatabase.db')

def sql_fetch(con):
   cursorObj = con.cursor()
   cursorObj.execute('create table if not exists projects(id integer, name text)')
   con.commit()

sql_fetch(con)

"""

Точно так же, чтобы проверить, существует ли таблица при удалении,
 мы используем «if not exists» с инструкцией DROP TABLE следующим образом:
cursorObj.execute('drop table if exists projects')

Также проверим, существует ли таблица, к которой нужно получить доступ, выполнив следующий запрос:


cursorObj.execute('SELECT name from sqlite_master WHERE type = "table" AND name ="employees"')

print(cursorObj.fetchall())

Если указанное имя таблицы не существует, будет возвращен пустой массив.

Удаление таблицы выполняется с помощью оператора DROP. Синтаксис оператора DROP выглядит следующим образом:
drop table table_name

Чтобы удалить таблицу, таблица должна существовать в БД.
 Поэтому рекомендуется использовать «if exists» с оператором DROP. Например, удалим таблицу employees:
"""


import sqlite3

con = sqlite3.connect('mydatabase.db')

def sql_fetch(con):
   cursorObj = con.cursor()
   cursorObj.execute('DROP table if exists employees')
   con.commit()
sql_fetch(con)


"""
2. Чтение документов

Сейчас мы рассмотрим работу с документами, независимо от того,
 скачиваем мы их в локальную папку или читаем по сети и извлекаем данные. Мы также познакомимся с
различными текстовыми кодировками, что позволит читать HTML-страницы на иностранных языках.
Кодировка документа указывает приложению — будь то операционная система компьютера или написанный вами код на Python,
 — как следует читать этот документ. Узнать кодировку обычно можно из расширения файла,
  хотя оно не обязательно соответствует кодировке. Я могу, например, сохранить файл myImage.jpg как myImage.txt,
   и проблем не возникнет — по крайней мере до тех пор, мы не попытаемся открыть его в текстовом редакторе.
    К счастью, подобные ситуации встречаются редко, как правило, достаточно знать расширение файла,
     в котором хранится документ, чтобы прочитать его правильно.
В своей основе любой документ содержит только нули и единицы. Затем вступают в действие алгоритмы кодирования.
 Они определяют такие вещи, как «сколько битов приходится на один символ» или «сколько битов занимает цвет пиксела»
  (в случае файлов с изображениями). Далее может подключаться уровень сжатия или
   некий алгоритм сокращения занимаемого места в памяти, как в случае с PNG-файлами.

Поначалу перспектива иметь дело с файлами, не относящимися к формату HTML,
 может выглядеть пугающе, однако будьте уверены: при подключении соответствующей
библиотеки Python располагает всеми необходимыми средствами для работы с любым форматом информации,
 который вам попадется. Единственное различие между файлами с текстом, видео и изображениями состоит в том,
  как интерпретируются их нули и единицы. Мы рассмотрим следующие часто встречающиеся типы файлов:
текст, CSV, PDF и документы Word.

Хранить файлы в виде обычного текста в Интернете кажется несколько необычным,
 однако есть много простых сайтов и сайтов старого образца с обширными хранилищами текстовых
файлов.
В большинстве браузеров эти текстовые файлы отлично отображаются, так что веб-скрапинг для них должен выполняться без проблем.
Для большинства простейших текстовых документов, таких как тестовый файл, расположенный по адресу
http://www.pythonscraping.com/pages/warandpeace/chapter1.txt,
можно использовать следующий метод:"""


from urllib.request import urlopen
textPage = urlopen('http://www.pythonscraping.com/pages/warandpeace/chapter1.txt')
print(textPage.read())


"""

Обычно, получая страницу с помощью urlopen, мы превращаем ее в объект BeautifulSoup,
 чтобы выполнить синтаксический анализ HTML-кода. В данном случае мы можем
прочитать страницу напрямую. Мы могли бы превратить ее в объект BeautifulSoup,
 однако это было бы нерационально: здесь нет HTML-разметки, которую стоило бы анализировать,
поэтому библиотека будет бесполезной. Прочитав текстовый файл как строку,
мы можем лишь проанализировать его аналогично любой другой строке, прочитанной в Python.
Правда, здесь не получится использовать HTML-теги в качестве контекстных подсказок, указывающих на то,
 какой текст нам действительно нужен, а какой можно отбросить. Это может стать проблемой,
  если из текстовых файлов требуется извлечь лишь определенную информацию.

В прошлых примерах мы использовали стандартные параметры настройки urlopen для чтения текстовых документов,
 которые встречаются в Интернете. Эти параметры
прекрасно подходят для большинства текстов на английском языке.
 Но если вам встретится документ на русском или арабском или даже всего лишь отдельное слово наподобие
re'sume' - могут возникнуть проблемы.
Рассмотрим, к примеру, такой код:

"""


from urllib.request import urlopen
textPage = urlopen('http://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt')
print(textPage.read())


"""

Этот код читает первую главу романа Л. Толстого «Война и мир»
 (где встречается текст на русском и французском языках) и выводит ее на экран.
В частности, на экран будет выведено следующее:
b"\xd0\xa7\xd0\x90\xd0\xa1\xd0\xa2\xd0\xac\xd0\x9f\xd0\x95\xd0\xa0\xd0\x92\xd0\
x90\xd0\xaf\n\nI\n\n\xe2\x80\x94 Eh bien, mon prince.

Открыв данную страницу в большинстве браузеров, мы тоже увидим абракадабру.
Это не поймут даже те, для кого русский язык является родным. 
Проблема в том, что Python пытается прочитать документ в кодировке ASCII,
 а браузер — в кодировке ISO-8859-1. И ни тот ни другой, конечно же, не предполагают, что кодировка данного документа — UTF-8.
Но можно явно задать кодировку строки как UTF-8, и тогда кириллические символы будут выведены правильно:
"""

from urllib.request import urlopen
textPage = urlopen('http://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt')
print(str(textPage.read(), 'utf-8'))


"""Применение в BeautifulSoup и Python выглядит так:"""


from urllib.request import urlopen

from bs4 import BeautifulSoup

html = urlopen('http://en.wikipedia.org/wiki/Python_(programming_language)')
bs = BeautifulSoup(html, 'html.parser')
content = bs.find('div', {'id':'mw-content-text'}).get_text()
content = bytes(content, 'UTF-8')
content = content.decode('UTF-8')
print(content)


"""
В Python все символы по умолчанию кодируются в UTF-8.
 У вас может возникнуть желание оставить все как есть и использовать кодировку UTF-8 во всех веб-скраперах, которые
вам доведется писать. В конце концов, UTF-8 будет одинаково хорошо поддерживать и символы в кодировке ASCII,
 и текст на иностранных языках. Однако важно помнить о 9 % сайтов, использующих ту или иную версию кодировки ISO,
  из-за которых вам не удастся полностью избежать этой проблемы.
К сожалению, в случае с текстовыми документами невозможно точно определить кодировку документа.
 Есть библиотеки, которые позволяют исследовать документ и сделать правильное предположение (используя некую логику,
  способную сделать вывод, что ÑˆÐ°ÑÑÐoÐ°Ð·Ñ, вероятно, не является словом), но они часто ошибаются.
  
К счастью, в случае с HTML-страницами кодировка обычно обозначена в теге, расположенном в разделе <head> сайта.
 У большинства сайтов, особенно англоязычных, есть такой тег:
<meta charset="utf-8" />
А, например, на сайте ECMA International (http://www.ecmainternational.org/) есть такой тег:
<META HTTP-EQUIV="Content-Type"
CONTENT="text/html; charset=iso-8859-1">
Если вы планируете выполнять активный веб-скрапинг, 
особенно многоязычных сайтов, то, вероятно, имеет смысл найти этот метатег и использовать рекомендованную в нем
кодировку для чтения контента страницы.

Ну и реализуем пример с использованием requests:
"""


import requests
from bs4 import BeautifulSoup

textPage = requests.get('http://en.wikipedia.org/wiki/Python_(programming_language)')

bs = BeautifulSoup(textPage.text, 'lxml')
content = bs.find('div', {'id':'mw-content-text'}).get_text()
content = bytes(content, 'UTF-8')
content = content.decode('UTF-8')
print(content)

"""
Домашняя работа
Спарсить первые два абзаца со странички 
http://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt 
с правильной кодировкой и сохранить их в txt файл
"""