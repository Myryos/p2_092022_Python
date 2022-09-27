from webbrowser import get
from bs4 import BeautifulSoup
import requests, sys

BASE_URL = 'http://books.toscrape.com/'

def getSoup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')
def newURL(str):
    array = str.split('/')
    return BASE_URL+array[4]+'/'+array[5]+'/'+array[6]+'/'+array[7]+'/'

def noTag(str):

    return str.get_text()

def getNavLinks(url):
    links = []
    soup = getSoup(url)
    navList = soup.find(class_='nav').find('li').find('ul').find_all('li')
    
    for nav in navList:
        links.append(nav.find('a')['href'])
    return links


def getAllLinksBook(url):
    newUrl = newURL(url)
    soup = getSoup(url)

    for title in soup.findAll('h3'):
        scrapPage(BASE_URL + 'catalogue/' + title.find('a')['href'].split('/')[3])
   
    if soup.find(class_='next') is not None:
        getAllLinksBook(newUrl + soup.find(class_='next').find('a')['href'])
    
    return 0

def scrapPage(url):
    soup = getSoup(url)
    

    for line in soup.findAll('tr'):
        for child in line.findAll('th'):
            if child.next_sibling is not None:
                print(child.next_element + child.find_next_sibling('td').get_text())
    return 0

def writeCSV(array):
    return 0


for nav in getNavLinks(BASE_URL + 'index.html'):
    getAllLinksBook(BASE_URL + nav)
