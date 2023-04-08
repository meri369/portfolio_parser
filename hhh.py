import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://docs.python.org'
URL = f'{BASE_URL}/3/library/index.html'


r = requests.get(URL)

bs = BeautifulSoup(r.text, 'html.parser')
url_list = bs.find_all('a')

for i in range(len(url_list)):
    url_list1 = BASE_URL + url_list[i].get('href')
    print(url_list1)