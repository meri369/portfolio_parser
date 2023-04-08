from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://www.python.org/')
bs = BeautifulSoup(html, 'html.parser')
nameList = bs.find_all('div', {'class': 'psf-widget'})

images = bs.find_all('img')
for image in images:
    print(image['src'])
for name in nameList:
    print(name.get_text())