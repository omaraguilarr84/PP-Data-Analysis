import requests
from bs4 import BeautifulSoup

url = 'https://www.pro-football-reference.com'

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

print(soup)