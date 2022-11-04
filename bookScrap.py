import csv
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests, os

BASE_URL = "http://books.toscrape.com/"


def get_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, "html.parser")


def get_rating(stars_classname):

    rating = 0

    if stars_classname == "One":
        rating = 1
    if stars_classname == "Two":
        rating = 2
    if stars_classname == "Three":
        rating = 3
    if stars_classname == "Four":
        rating = 4
    if stars_classname == "Five":
        rating = 5
    return rating


def get_navlinks(url):
    links = []
    soup = get_soup(url)
    nav_list = soup.find(class_="nav").find("li").find("ul").find_all("li")

    for nav in nav_list:
        links.append(nav.find("a")["href"])
    return links


def get_all_next_pages(soup):
    urls = []
    if soup.find(class_="current") is not None:
        test = soup.find(class_="current").get_text()
        test = test.split()
        page_counter = 2
        while page_counter <= int(test[3]):
            urls.append(f"page-{page_counter}.html")
            page_counter += 1
    return urls


def get_books_scraped(soup, category, url):
    for title in soup.findAll("h3"):
        book_url = urljoin(url, title.find("a")["href"])
        scrape_page(book_url, category)


def scrape_page(url, category):
    """ "Return the data from a book in a dictionnary"""
    soup = get_soup(url)
    title = soup.find("h1").get_text()
    product_description = ""
    img_url = urljoin(url, soup.find(class_="item active").find("img")["src"])

    star_ratings = soup.find(class_="star-rating")["class"]

    rating = get_rating(star_ratings[1])

    if soup.find(id="product_description") is not None:
        product_description = (
            soup.find(id="product_description").find_next("p").get_text()
        )
    t = title.replace("/", " ")
    scraped_data = {
        "product_page_url": url,
        "title": t,
        "product_description": product_description,
        "category": category,
        "review_rating": rating,
        "image_url": img_url,
    }
    for child in soup.findAll("th"):
        if child.next_sibling is not None:
            brother = child.find_next_sibling("td").get_text()
            if child.get_text() == "Availability":
                brother = brother.split(" ")[2].split("(")[1]
            scraped_data[child.get_text()] = brother
    
    download_image(scraped_data["image_url"], scraped_data["title"])
    write_csv(scraped_data)

def write_csv(book):
    """Create a CSV File or open an CSV File and add datas from books"""
    mode = ""
    if os.path.isfile(f"datas/{book['category']}.csv"):
        mode = "a"
    else:
        mode = "w"

    with open(f"datas/{book['category']}.csv", mode) as csvfile:
        fieldnames = [
            "product_page_url",
            "universal_ product_code",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if mode == "w":
            writer.writeheader()

        writer.writerow(
            {
                "product_page_url": book["product_page_url"],
                "universal_ product_code": book["UPC"],
                "title": book["title"],
                "price_including_tax": book["Price (incl. tax)"],
                "price_excluding_tax": book["Price (excl. tax)"],
                "number_available": book["Availability"],
                "product_description": book["product_description"],
                "category": book["category"],
                "review_rating": book["review_rating"],
                "image_url": book["image_url"],
            }
        ),


def download_image(url, title):
    image = open(f"medias/images/{title}.jpg", "wb")
    response = requests.get(url)
    image.write(response.content)
    image.close()


def init_folders():
    """ "Initialize the folder needed for the datas and medias"""
    if not os.path.exists("datas"):
        os.mkdir("datas")
    if not os.path.exists("medias"):
        os.mkdir("medias")
    if not os.path.exists("medias/images"):
        os.mkdir("medias/images")


def start_scraping():
    url_init = urljoin(BASE_URL, "index.html")
    for nav in get_navlinks(url_init):
        url_nav = urljoin(BASE_URL, nav)
        soup = get_soup(url_nav)
        category = soup.find("h1").get_text()
        next_pages = get_all_next_pages(soup)
        get_books_scraped(soup, category, url_nav)
        for page in next_pages:
            url_page = urljoin(url_nav, page)
            soup = get_soup(url_page)
            get_books_scraped(soup, category, url_nav)

init_folders()
start_scraping()