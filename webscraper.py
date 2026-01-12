import requests
from bs4 import BeautifulSoup

url = 'https://fdic.gov/laws-and-regulations/fdic-law-regulations-related-acts'
response = requests.get(url)
html_content = response.content 


soup = BeautifulSoup(html_content, 'html.parser')
html_content = soup.prettify()

textFormat = soup.get_text()
#print(textFormat)
print(html_content)

# no need scrape this website :(
# have to use their dev api 

websites = []

'''

We dont really need to scrape the website, we can just use their api to get the documents we need.

'''
