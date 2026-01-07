import requests
from bs4 import BeautifulSoup

url = 'https://www.federalregister.gov'
response = requests.get(url)
html_content = response.content 


soup = BeautifulSoup(html_content, 'html.parser')
print(soup.prettify())

# cant scrape this website :(

# have to use their dev api 
