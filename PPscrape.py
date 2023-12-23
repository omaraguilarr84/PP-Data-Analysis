import requests
from bs4 import BeautifulSoup

user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_9) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15'
]
url = 'https://www.pro-football-reference.com/years/2023/passing.htm'
headers = {'User-Agent': user_agents[0]}

html = requests.get(url, headers=headers)

soup = BeautifulSoup(html.content, 'html.parser')
