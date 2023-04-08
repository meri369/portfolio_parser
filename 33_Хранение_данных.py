"""Урок 33.1 Хранение данных

1. Хранение данных
Несмотря на то что вывод данных на терминал доставляет массу удовольствия, он не слишком полезен для агрегирования и анализа данных.
В большинстве случаев, чтобы работа удаленных веб-скраперов приносила пользу,
необходимо иметь возможность сохранять получаемую от них информацию.
Далее мы рассмотрим три основных метода управления данными, которых вам будет достаточно практически для любого случая.
Хотите запустить серверную часть сайта или создать собственный API?
 Тогда, возможно, веб-скраперы должны записывать информацию в базу данных.
Нужен быстрый и простой способ собирать документы из Интернета и сохранять их на жестком диске?
Вероятно, для этого стоит создать файловый поток.
Требуется время от времени отправлять предупреждения или раз в день передавать сводные данные?
Тогда отправьте себе письмо по электронной почте!

Возможность взаимодействовать с большими объемами данных и хранить их невероятно важна не только для веб-скрапинга,
но и практически для любого современного программного обеспечения.

Медиафайлы
Есть два основных способа хранения медиафайлов: сохранить ссылку или скачать сам файл. Чтобы сохранить файл по ссылке,
нужно сохранить URL, по которому находится этот файл.
Данный способ имеет следующие преимущества:
• веб-скраперы работают намного быстрее и требуют гораздо меньшей пропускной способности, если им не нужно скачивать файлы;
• сохраняя только URL, вы экономите место на своем компьютере;
• проще написать код, который не скачивает файлы, а лишь сохраняет их URL;
• избегая скачивания больших файлов, вы уменьшаете нагрузку на сервер, на котором размещен сканируемый ресурс.

Но есть и недостатки.
• Встраивание URL в ваш сайт или приложение называется горячими ссылками; это легкий способ нажить себе неприятности в Интернете.
• Вы вряд ли захотите размещать на чужих серверах мультимедийные ресурсы, которые используются в ваших приложениях.
• Файл, размещенный по определенному URL, может измениться.
Это может привести к нелепой ситуации, если, к примеру, разместить картинку, расположенную по этому
адресу, в публичном блоге. Если сохранить URL, рассчитывая позже скачать и изучить сам файл,
то однажды данный файл могут удалить или заменить чем-нибудь совершенно
неподходящим.
• Настоящие браузеры не просто получают HTML-код страницы и двигаются дальше.
Они также скачивают все ресурсы, необходимые для отображения данной страницы.

Скачивая файлы, вы делаете действия веб-скрапера больше похожими на действия человека,
который просматривает сайт, — это может стать преимуществом.
Принимая решение, сохранять ли сам файл или только его URL, следует спросить себя:
намерены ли вы просматривать или читать этот файл чаще чем один-два раза? Или же со
временем у вас накопится целая база данных с такими файлами, которая большую часть времени будет лежать на ПК мертвым грузом?

В библиотеке urllib, используемой для извлечения контента веб-страниц, также содержатся функции для получения содержимого файлов.
Следующая программа с помощью urllib.request.urlretrieve скачивает изображения с удаленного URL:

"""
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com')
bs = BeautifulSoup(html, 'html.parser')
imageLocation = bs.find('img', class_='pagelayer-img pagelayer-animation-{{anim_hover}}')['src']
urlretrieve(imageLocation, 'logo.jpg')

"""Эта программа скачивает картинку с логотипом, размещенную по адресу http://pythonscraping.com,
и сохраняет ее под именем logo.jpg в том же каталоге, из которого запускается скрипт.
Данный код отлично справляется с задачей, когда нужно скачать только один файл с заранее известным именем и расширением.
Но большинство веб-скраперов не
ограничиваются скачиванием одного файла. Следующая программа скачивает с главной страницы http://pythonscraping.com все файлы,
на которые указывает ссылка в атрибуте src любого тега, если это внутренняя ссылка:
"""
import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

downloadDirectory = 'downloaded/'
baseUrl = 'https://pythonscraping.com/'


def getDownloadPath(baseUrl, absoluteUrl, dowloadDirectory):
   path = absoluteUrl.replace('https://', '')
   path = path.replace(baseUrl, '')
   path = dowloadDirectory + path
   directory = os.path.dirname(path)
   print(directory)
   if not os.path.exists(directory):
       os.makedirs(directory)
   return path


html = urlopen('https://pythonscraping.com/')
soup = BeautifulSoup(html, 'lxml')
downloadList = soup.find_all(src=True)
print(downloadList)
for download in downloadList:
   fileUrl = download['src']
    print(fileUrl)
   if 'uploads' in fileUrl:
       print(fileUrl)
       urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, downloadDirectory))


"""

Представленный выше скрипт скачивает на жесткий диск вашего компьютера все подряд,
включая случайные скрипты bash, .exe-файлы и другие потенциально вредоносные программы.
Рассмотренная выше программа написана исключительно для примера;
ее нельзя устанавливать в рабочей среде без более тщательной проверки имен файлов
и ее следует запускать только из учетной записи с ограниченными правами.

В этом скрипте с помощью лямбда-функции мы выбираем на главной странице сайта все теги,
имеющие атрибут src, а затем очищаем и нормализуем URL, чтобы получить абсолютный путь для каждого скачиваемого файла
(и гарантированно отсеять все внешние ссылки). Затем каждый файл скачивается по своей ссылке и помещается на компьютер
в локальную папку downloaded.
Обратите внимание: для быстрой ссылки на каталог, в который помещаются результаты каждого скачивания,
а также для создания при необходимости недостающих каталогов
используется Python-модуль os. 
Он играет роль интерфейса между Python и операционной системой,
позволяя ей управлять путями к файлам, создавать каталоги, получать информацию о работающих процессах и переменных среды и т.п.

Подобно тому как веб-страницы передаются по протоколу HTTP,
электронная почта пересылается по протоколу SMTP (Simple Mail Transfer Protocol, простой протокол электронной почты).
И точно так же, как для отправки веб-страниц по HTTP
мы используем клиент веб-сервера, для отправки и получения электронной почты серверы задействуют различные почтовые клиенты.
Несмотря на то что отправка электронной почты в Python осуществляется сравнительно просто, эта операция требует доступа к серверу,
на котором работает SMTP.
В следующем примере,  который напишем, предполагается, что SMTP-клиент используется локально.
(Чтобы модифицировать этот код для удаленного SMTP-клиента, замените localhost адресом удаленного сервера.)
Для отправки электронного письма с помощью Python достаточно всего девяти строк кода:
"""
import smtplib
from email.mime.text import MIMEText
msg = MIMEText('The body of the email is here')
msg['Subject'] = 'An Email Alert'
msg['From'] = 'example@yandex.ru'
msg['To'] = 'example1@yandex.ru'
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()


"""
В Python есть два важных пакета для отправки электронной почты: smtplib и email.
Python-модуль email содержит полезные функции форматирования для создания готовых к отправке пакетов электронной почты. 
Применяемый здесь объект MIMEText
создает пустое электронное письмо, отформатированное для передачи по низкоуровневому протоколу MIME (Multipurpose Internet Mail Extensions,
многоцелевые расширения почтовой
интернет-службы), через который устанавливаются SMTP-соединения более высокого уровня. 
Объект MIMEText содержит адреса электронной почты, тело и заголовок, служащие в
Python для создания правильно отформатированного электронного письма.

Пакет smtplib содержит информацию для обработки соединения с сервером. Как и при соединении с сервером базы данных,
это соединение, будучи созданным и использованным,
должно разрываться, чтобы не создавалось слишком большого количества соединений.

Учитель:  CSV (comma-separated values — «значения, разделенные запятыми») — 
один из самых популярных форматов файлов для хранения табличных данных. Благодаря своей простоте этот формат поддерживается Microsoft Excel и многими другими приложениями. Ниже показан пример совершенно правильного содержимого CSV-файла:
fruit,cost
apple,1.00
banana,0.30
pear,1.25

Как и в Python, здесь важны разделители: строки отделяются друг от друга символом новой строки,
а столбцы внутри строки — запятыми (отсюда и название «разделенные запятыми»). 
В других вариантах CSV-файлов (иногда называемых character-separated values — «файлы значений,разделенных символами») для разделения строк используются табуляции и другие символы, но эти форматы менее распространены и поддерживаются не так широко.
Если вы хотите скачивать CSV-файлы прямо из Интернета и хранить их локально, не анализируя и не изменяя,
то вам подойдут и прошлые примеры скрапперов. Скачайте эти файлы, как любые другие, и сохраните их в формате CSV, используя методы из прошлых занятий.
Python позволяет легко изменять и даже создавать CSV-файлы с нуля с помощью библиотеки csv:
"""

import csv
csvFile = open('test.csv', 'w+')
try:
   writer = csv.writer(csvFile)
   writer.writerow(('number', 'number plus 2','number times 2'))
   for i in range(10):
       writer.writerow( (i, i+2, i*2))
finally:
   csvFile.close()


"""
Создание файла в Python - практически безошибочная процедура. При отсутствии
файла test.csv Python автоматически создаст его (но не каталог). Если же такой файл уже есть, то Python перезапишет test.csv, внеся в него новые данные.
После выполнения этой программы должен получиться следующий CSV-файл:
number,number plus 2,number times 2
0,2,0
1,3,2
2,4,4
…

Одна из самых популярных задач веб-скрапинга — скачать HTML-таблицу и сохранить ее в виде CSV-файла. Сравнение текстовых редакторов в «Википедии» (https://en.wikipedia.org/wiki/Comparison_of_text_editors) представляет собой весьма сложную HTML-таблицу с выделением ячеек разными цветами, а также со ссылками,
сортировкой и другим HTML-мусором, который необходимо будет вычистить, прежде чем записывать данные в формат CSV. Активно используя BeautifulSoup и функцию get_text(),
мы можем сделать это менее чем за 20 строк кода:
"""

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://en.wikipedia.org/wiki/Comparison_of_text_editors')
bs = BeautifulSoup(html, 'html.parser')
# Основная сравнительная таблица сейчас является первой на странице.
table = bs.find_all('table', {'class': 'wikitable'})[0]
rows = table.find_all('tr')
csvFile = open('editors.csv', 'wt+', encoding="utf-8")
writer = csv.writer(csvFile)
try:
   for row in rows:
       csvRow = []
       for cell in row.find_all(['td', 'th']):
           csvRow.append(cell.get_text())
       writer.writerow(csvRow)
finally:
   csvFile.close()

"""
В результате должен получиться правильно отформатированный CSV-файл, сохраненный на локальном компьютере под именем editors.csv.
Теперь поговорим о варианте сохранения в базе данных. Давайте рассмотрим как с ней работать в Python.
База данных — это упорядоченный набор структурированной информации или данных,
которые обычно хранятся в электронном виде в компьютерной системе. База данных обычно управляется системой управления базами данных (СУБД).
Данные вместе с СУБД, а также приложения, которые с ними связаны, называются системой баз данных, или, для краткости, просто базой данных.

Базы данных и электронные таблицы (в частности, Microsoft Excel) предоставляют удобные способы хранения информации.
Основные различия между ними заключаются в следующем.
Способ хранения и обработки данных
Полномочия доступа к данным
Объем хранения данных
Электронные таблицы изначально разрабатывались для одного пользователя, и их свойства отражают это.
Они отлично подходят для одного пользователя или небольшого числа пользователей, 
которым не нужно производить сложные операции с данными.
С другой стороны, базы данных предназначены для хранения гораздо больших наборов упорядоченной информации—иногда огромных объемов.
Базы данных дают возможность множеству пользователей в одно и то же время быстро и безопасно получать доступ к данным и запрашивать их,
используя развитую логику и язык запросов.

Существует множество различных типов баз данных. Выбор наилучшей базы данных для конкретной компании зависит от того,
как она намеревается использовать данные.
Реляционные базы данных Реляционные базы данных стали преобладать в 1980-х годах.
Данные в реляционной базе организованы в виде таблиц, состоящих из столбцов и строк.
Реляционная СУБД обеспечивает быстрый и эффективный доступ к структурированной информации.
Объектно-ориентированные базы данных Информация в объектно-ориентированной базе данных представлена в форме объекта,
как в объектно-ориентированном программировании.
Распределенные базы данных Распределенная база данных состоит из двух или более частей, расположенных на разных серверах.
Такая база данных может храниться на нескольких компьютерах.
Хранилища данных Будучи централизованным репозиторием для данных, хранилище данных представляет собой тип базы данных,
специально предназначенной для быстрого выполнения запросов и анализа.
Базы данных NoSQL База данных NoSQL, или нереляционная база данных,
дает возможность хранить и обрабатывать неструктурированные или слабоструктурированные данные (в отличие от реляционной базы данных,
задающей структуру содержащихся в ней данных). Популярность баз данных NoSQL растет по мере распространения и усложнения веб-приложений.
Графовые базы данных Графовая база данных хранит данные в контексте сущностей и связей между сущностями.
Базы данных OLTP. База данных OLTP — это база данных предназначенная для выполнения бизнес-транзакций,
выполняемых множеством пользователей.
Это лишь некоторые из десятков типов баз данных, используемых в настоящее время. 
Другие, менее распространенные базы данных, предназначены для очень специфических научных, финансовых и иных задач.

В данном случае мы будем знакомиться с SQL базами данных, а непосредственно SQLite.
Данная база данных не требует установки на компьютер и взаимодействует с Python с помощью модуля sqlite3.

Модуль sqlite3 реализует интерфейс доступа к внутрипроцессной базе данных SQLite.
База данных SQLite спроектирована таким образом, чтобы ее можно было встраивать в приложения,
а не использовать отдельную серверную программу, такую как MySQL, PostgreSQL или Oracle.
SQLite — быстрая, тщательно протестированная и гибкая база данных,
что делает ее весьма удобной для прототипирования и производственного развертывания в случае некоторых приложений.

База данных SQLite хранится в файловой системе в виде одиночного файла. Библиотека управляет доступом к этому файлу,
включая его блокирование c целью предотвращения повреждения данных, когда одновременно несколько программ пытаются записать данные в файл.
База данных создается при первой попытке доступа к файлу, но ответственность за создание таблицы определений, или схемы базы данных,
возлагается на приложение.
В этом примере программа сначала осуществляет поиск файла базы данных, прежде чем открыть его c помощью функции connect (),
поэтому ей известно, в каких случаях следует создавать схему для новых баз данных.
"""

import os
import sqlite3
db_filename = 'todo.db'
db_is_new = not os.path.exists(db_filename)
conn = sqlite3.connect(db_filename)
if db_is_new:
   print('Создана новая база')
else:
   print('База данных уже существует.')
conn.close()


"""Выполнение этого кода два раза подряд показывает, что в том случае, когда файл не существует, создается пустой файл.
После создания нового файла базы данных следующим шагом является создание схемы для определения таблиц в базе данных."""

import os
import sqlite3
db_filename = 'todo.db'
schema_filename = 'todo_schema.sql'
db_is_new = not os.path.exists(db_filename)
with sqlite3.connect(db_filename) as conn:
   if db_is_new:
       print('Creating schema')
       with open(schema_filename, 'rt') as f:
           schema = f.read()
       conn.executescript(schema)
       print('Inserting initial data')
       conn.executescript("""
       insert into project (name, description, deadline)
       values ('pymotw', ’Python Module of the Week’,
       '2022-11-01’);
       insert into task (details, status, deadline, project)
       values ('write about select', 'done', '2022-04-25',
       'pymotw');
       insert into task (details, status, deadline, project)
       values ('write about random', 'waiting', '2022—08—22',
       'pymotw');
       insert into task (details, status, deadline, project)
       values ('write about sqlite3', 'active', '2021—07—31',
       'pymotw');
       """)
   else:
       print('Database exists, assume schema does, too.')




Вслед за созданием таблиц выполняются инструкции вставки, c помощью которых создается пробный проект и относящиеся к нему задачи.
SQLite для Python предлагает меньше типов данных, чем есть в других реализациях SQL.
С одной стороны, это накладывает ограничения, но, с другой стороны, в SQLite многое сделано проще. Вот основные типы:
NULL — значение NULL
INTEGER — целое число
REAL — число с плавающей точкой
TEXT — текст
BLOB — бинарное представление крупных объектов, хранящееся в точности с тем, как его ввели

Разберем создание базы данных и таблицы подробнее. Есть несколько способов создания базы данных в Python с помощью SQLite.
Для этого используется объект Connection, который и представляет собой базу. Он создается с помощью функции connect().
Создадим файл .db, поскольку это стандартный способ управления базой SQLite.
Файл будет называться test.db. За соединение будет отвечать переменная conn.

conn = sqlite3.connect('test.db')

Эта строка создает объект connection, а также новый файл orders.db в рабочей директории.
Если нужно использовать другую, ее нужно обозначить явно:

conn = sqlite3.connect('ПУТЬ-К-ПАПКИ/test.db')


Если файл уже существует, то функция connect осуществит подключение к нему.
Функция connect создает соединение с базой данных SQLite и возвращает объект, представляющий ее.

Еще один способ создания баз данных с помощью SQLite в Python — создание их в памяти.
Это отличный вариант для тестирования, ведь такие базы существуют только в оперативной памяти.

conn = sqlite3.connect(:memory:)


После создания объекта соединения с базой данных нужно создать объект cursor. Он позволяет делать SQL-запросы к базе.
Используем переменную cur для хранения объекта:

cur = conn.cursor()


Теперь выполнять запросы можно следующим образом:

cur.execute("ВАШ-SQL-ЗАПРОС-ЗДЕСЬ;")


Обратите внимание на то, что сами запросы должны быть помещены в кавычки — это важно.
Это могут быть одинарные, двойные или тройные кавычки.
Последние используются в случае особенно длинных запросов, которые часто пишутся на нескольких строках.

Давайте разберем как создать таблицу, в которой у нас есть имя фамилия пол, ну и порядковый номер. Для этого необходимо создать запрос

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INT PRIMARY KEY,
   fname TEXT,
   lname TEXT,
   gender TEXT);
""")
conn.commit()


В коде выполняются следующие операции:
Функция execute отвечает за SQL-запрос
SQL генерирует таблицу users
IF NOT EXISTS поможет при попытке повторного подключения к базе данных. Запрос проверит, существует ли таблица.
Если да — проверит, ничего ли не поменялось.
Создаем первые четыре колонки: userid, fname, lname и gender. Userid — это основной ключ.
Сохраняем изменения с помощью функции commit для объекта соединения.

Создадим еще одну таблицу

cur.execute("""CREATE TABLE IF NOT EXISTS orders(
   orderid INT PRIMARY KEY,
   date TEXT,
   userid TEXT,
   total TEXT);
""")
conn.commit()


Полный код

import os
import sqlite3


conn = sqlite3.connect('todo.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
  userid INT PRIMARY KEY,
  fname TEXT,
  lname TEXT,
  gender TEXT);
""")
cur.execute("""CREATE TABLE IF NOT EXISTS orders(
  orderid INT PRIMARY KEY,
  date TEXT,
  userid TEXT,
  total TEXT);
""")

conn.commit()




После исполнения этих двух скриптов база данных будет включать две таблицы. Теперь можно добавлять данные.


Дополнительно
Если на уроке остается время, то ученикам можно предложить начать прорешивать домашнее задание.

Домашняя работа
Реализовать парсер википедии, который сохраняет страницу в виде csv файла




