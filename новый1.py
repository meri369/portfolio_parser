import requests
import lxml
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

BASE_URL = 'https://docs.python.org'
url = f'{BASE_URL}/3/library/index.html'

r = requests.get(url=url)
if not r.raise_for_status():
     bs=BeautifulSoup(r.text,"lxml")
     url_list=bs.find_all("a")

     print(url_list)
     #print(r.text)
