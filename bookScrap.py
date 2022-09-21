from operator import concat
from types import NoneType
from webbrowser import get
from bs4 import BeautifulSoup;
import requests, sys

BASE_URL = 'http://books.toscrape.com/'
genre = ''
nextURL = ''

links = []

def getAllLinksBook(url):

    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html5lib')

    titles = soup.findAll('h3')

    for title in titles:
        links.append(title.find('a')['href'])
    
   
    if soup.find(class_='next') is not None:
        nextURL = soup.find(class_='next').find('a')['href']
    else:
        return 0
    
    
    if "catalogue/" in nextURL:
        getAllLinksBook(BASE_URL + nextURL)
    else:
        getAllLinksBook(BASE_URL + "catalogue/" + nextURL)

getAllLinksBook(BASE_URL)

print(len(links))






