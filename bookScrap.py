import csv
from urllib.parse import urlparse, urljoin
from webbrowser import get
from bs4 import BeautifulSoup
import requests, sys, os

BASE_URL = 'http://books.toscrape.com/'



def get_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def get_rating(stars_classname):

    rating = 0

    if stars_classname == 'One':
        rating = 1
    if stars_classname == 'Two':
        rating = 2
    if stars_classname == 'Three':
        rating = 3
    if stars_classname == 'Four':
        rating = 4
    if stars_classname == 'Five':
        rating = 5
    return rating 

def get_navlinks(url):
    links = []
    soup = get_soup(url)
    nav_list = soup.find(class_='nav').find('li').find('ul').find_all('li')
    
    for nav in nav_list:
        links.append(nav.find('a')['href'])
    return links


def get_books_scraped(url):
    soup = get_soup(url)
    category = soup.find('h1').get_text()

    dict_book = []

    for title in soup.findAll('h3'):
        """"
        catalogue_url = urljoin(BASE_URL, "catalogue/")
        print(catalogue_url)
        print("Test : " + urljoin(CATALOGE_URL, title.find('a')['href']))
        scrap_page(urljoin(BASE_URL + "catalogue/", title.find('a')['href']))
    
        """
        ##print(BASE_URL + 'catalogue/' + title.find('a')['href'].split('/')[3])
        dict_book.append(scrape_page(urljoin(url, title.find('a')['href']), category))
        ##print("Ca marche : " + str(x))
   
    if soup.find(class_='next') is not None:
        """print(f"{BASE_URL = }" )
        print(f"{url =}")
        print(f"{urljoin(url, soup.find(class_='next').find('a')['href']) = }")""" ##Exemple a garder !
        get_books_scraped(urljoin(url, soup.find(class_='next').find('a')['href']))
    ##write_csv(dict_book, category)
    return dict_book

def scrape_page(url, category):
    soup = get_soup(url)
    title = soup.find('h1').get_text()
    product_description = ""
    category = category
    img_url = urljoin(url, soup.find(class_='item active').find('img')['src'])

    star_ratings = soup.find(class_='star-rating')['class']

    rating = get_rating(star_ratings[1])

    if soup.find(id='product_description') is not None:
         product_description = soup.find(id='product_description').find_next('p').get_text()
    
    """print("URL : " + url)
    print("Titre : " + title)
    print("Desc : " + product_dscp)
    print("Catagory : " + category)
    print("Rating : " + str(rating))
    print("Img_URL : " + img_url)"""

    scraped_data = {
        "product_page_url": url, 
        "title": title, 
        "product_description":  product_description,
        "category":category,
        "review_rating": rating,
        "image_url":img_url
        }
    ##print(scraped_data)
    for child in soup.findAll('th'):
        if child.next_sibling is not None:
            brother = child.find_next_sibling('td').get_text()
            if child.get_text() == "Availability":
                brother = brother.split(" ")[2].split("(")[1]
            scraped_data[child.get_text()] = brother
    return scraped_data

def write_csv(book):
    if not os.path.exists("datas"):
        os.mkdir("datas")
    if os.getcwd() != "/Users/herve/OC Project/p2_092022_Python/datas":
        os.chdir('datas')
    mode = ''
    if os.path.isfile(f"{book['category']}.csv"):
        mode = 'a'
        with open(f"{book['category']}.csv", mode) as csvfile:
            fiednames = [
                'product_page_url', 
                'universal_ product_code', 
                'title',
                'price_including_tax',
                'price_excluding_tax',
                'number_available',
                'product_description',
                'category',
                'review_rating',
                'image_url'
                ]
            writer = csv.DictWriter(csvfile, fieldnames=fiednames)
            writer.writerow({
                'product_page_url': book['product_page_url'],
                'universal_ product_code' : book["UPC"],
                'title': book["title"],
                'price_including_tax': book["Price (incl. tax)"],
                'price_excluding_tax': book["Price (excl. tax)"],
                'number_available': book["Availability"],
                'product_description': book["product_description"],
                'category': book["category"],
                'review_rating':book["review_rating"],
                'image_url': book['image_url']}),

    else:
        mode = 'w'
        with open(f"{book['category']}.csv", mode) as csvfile:
            fiednames = [
                'product_page_url', 
                'universal_ product_code', 
                'title',
                'price_including_tax',
                'price_excluding_tax',
                'number_available',
                'product_description',
                'category',
                'review_rating',
                'image_url'
                ]
            writer = csv.DictWriter(csvfile, fieldnames=fiednames)

            writer.writeheader()
        
            writer.writerow({
                'product_page_url': book['product_page_url'],
                'universal_ product_code' : book["UPC"],
                'title': book["title"],
                'price_including_tax': book["Price (incl. tax)"],
                'price_excluding_tax': book["Price (excl. tax)"],
                'number_available': book["Availability"],
                'product_description': book["product_description"],
                'category': book["category"],
                'review_rating':book["review_rating"],
                'image_url': book['image_url']}),
    os.chdir("../")

def dl_image(url, title):
    if not os.path.exists("medias"):
        os.mkdir("medias")
    if not os.path.exists("medias/images"):
        os.mkdir("medias/images")
    if os.getcwd() != "/Users/herve/OC Project/p2_092022_Python/medias/images":
        os.chdir('medias/images')
    image = open(f'{title}.jpg', 'wb')
    response = requests.get(url)
    image.write(response.content)
    image.close()
    os.chdir("../../")

books_scraped = []

for nav in get_navlinks(BASE_URL + 'index.html'):
    books_scraped.append(get_books_scraped(BASE_URL + nav))

for books in books_scraped:
    for book in books:
        print(os.getcwd())
        dl_image(book['image_url'], book['title'])
        print(os.getcwd())
        write_csv(book)
