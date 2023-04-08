import requests
from bs4 import BeautifulSoup

url = 'https://docs.python.org/3/library/index.html'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a')
for link in links:
    href = link.get('href')
    if href.startswith('http'):
        print(href)