import requests
import lxml
from bs4 import BeautifulSoup

BASE_URL = 'https://www.kinopoisk.ru'
url = f'{BASE_URL}/media/article/4007433/'

r = requests.get(url=url)
if not r.raise_for_status(): # если ошибки нет
    bs = BeautifulSoup(r.text, 'lxml')
    content = bs.find('div', class_='media-article__body-wrapper') #find- ищем 1 элемент \ findall-ищем вообще все
    list_films = content.find_all('div', class_='stk-grid stk-theme_27251__mb_cus_72')
    article1 = list_films[0]
    title = article1.h2.get_text() # получить текст
    content = article1.find('p', class_='stk-reset stk-theme_27251__mb_cus_36').get_text()
    article_url = article1.a.get('href')
    article_url = BASE_URL + article_url # обядиняиться ссылки
    image = article1.img.get('src')
    print(f'Заголовок {title}')
    print(content)
    print(article_url)#!!!!
    print(image)
