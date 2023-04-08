'''Реализовать простой парсер выводящий все встречающиеся ссылки
 со страницы https://docs.python.org/3/library/index.html'''
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://docs.python.org/3/library/index.html'
url = f'{BASE_URL}/3/library/index.html'

r = requests.get(url=url)
bs = BeautifulSoup(r.text, 'html')

c=bs.find_all("a")

#c_url = c.a.get('href')
for i in range(c):
    a = i.get('href)
    c_url= BASE_URL + a
    print(c_url)