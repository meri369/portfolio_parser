import requests

from bs4 import BeautifulSoup

url = 'https://ru.wikipedia.org/wiki/Заглавная_страница'

html = requests.get(url)
bs = BeautifulSoup(html.text, 'html.parser')
print(bs.title)
#print(bs.body.div)