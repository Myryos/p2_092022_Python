import string
from types import NoneType
from urllib.parse import urlparse, urljoin
from webbrowser import get
from bs4 import BeautifulSoup
import requests, sys

BASE_URL = 'http://books.toscrape.com/'



def get_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def no_tag(str):

    return str.get_text()

def get_rating(str):

    r = 0

    if str == 'One':
        r = 1
    if str == 'Two':
        r = 2
    if str == 'Three':
        r = 3
    if str == 'Four':
        r = 4
    if str == 'Five':
        r = 5
    return r 

def get_navlinks(url):
    links = []
    soup = get_soup(url)
    navList = soup.find(class_='nav').find('li').find('ul').find_all('li')
    
    for nav in navList:
        links.append(nav.find('a')['href'])
    return links


def get_all_links_book(url):
    newUrl = urljoin(BASE_URL, url)
    soup = get_soup(url)

    dict_book ={}
    x = 0

    for title in soup.findAll('h3'):
        """"
        catalogue_url = urljoin(BASE_URL, "catalogue/")
        print(catalogue_url)
        print("Test : " + urljoin(CATALOGE_URL, title.find('a')['href']))
        scrap_page(urljoin(BASE_URL + "catalogue/", title.find('a')['href']))
        """

        ##print(BASE_URL + 'catalogue/' + title.find('a')['href'].split('/')[3])
        dict_book["Livre #"+str(x)] = scrap_page(BASE_URL + 'catalogue/' + title.find('a')['href'].split('/')[3])
        ##print("Ca marche : " + str(x))
        x += 1 
   
    if soup.find(class_='next') is not None:
        get_all_links_book(newUrl + soup.find(class_='next').find('a')['href'])
    print(dict_book)
    return 0

def scrap_page(url):
    soup = get_soup(url)

    title = soup.find('h1').get_text()
    product_dscp = ""
    rating = 0
    category = soup.find(class_='breadcrumb').find_all('li')[2].get_text()
    img_url = urljoin(BASE_URL, soup.find(class_='item active').find('img')['src'])

    star_ratings = soup.find(class_='star-rating')['class']

    rating = get_rating(star_ratings[1])

    if soup.find(id='product_description') is not None:
        product_dscp = soup.find(id='product_description').find_next('p').get_text()

    dict_scraped = {
        "product_page_url": url, 
        "title": title, 
        "product_description": product_dscp,
        "catagory":category,
        "review_rating": rating,
        "image_url":img_url
        }
    for child in soup.findAll('th'):
        if child.next_sibling is not None:
            dict_scraped[child.get_text()] = child.find_next_sibling('td').get_text()
    return dict_scraped

def write_csv(array):
    return 0


for nav in get_navlinks(BASE_URL + 'index.html'):
    get_all_links_book(BASE_URL + nav) 

    ## passe du camelCame to snake_case
    ## Finir l'ecriture du scrap page renvois un dictionnaire d'un book