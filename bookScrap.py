from operator import le
from types import NoneType
from webbrowser import get
from bs4 import BeautifulSoup
import requests, sys

BASE_URL = 'http://books.toscrape.com/catalogue/'
genre = ''
nextURL = ''

links = []


def getSoup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html5lib')
def getAllLinksBook(url):
    soup = getSoup(url)

    titles = soup.findAll('h3')

    for title in titles:
        links.append(title.find('a')['href'])
    
   
    if soup.find(class_='next') is not None:
        nextURL = soup.find(class_='next').find('a')['href']
        getAllLinksBook(BASE_URL + genre + nextURL)
    else:
        return 0
def scrapPage(url):
    soup = getSoup(url)

    allLine = soup.findAll('tr')

    for line in allLine:
        print(line.findAll('td'))
    
    return 0


match input("Genre de livre ? (pour la liste des genres ce referre au README.md)"):
    case "1":
        genre = "category/books_1/"
    case "2":
        genre = "category/books/travel_2/"
    case "3":
        genre = "category/books/mystery_3/"
    case "4":
        genre = "category/books/historical-fiction_4/"
    case "5":
        genre = "category/books/sequential-art_5/"
    case "6":
        genre = "category/books/classics_6/"
    case "7":
        genre = "category/books/philosophy_7/"
    case "8":
        genre = "category/books/romance_8/"
    case "9":
        genre = "category/books/womens-fiction_9/"
    case "10":
        genre = "category/books/fiction_10/"
    case "11":
        genre = "category/books/childrens_11/"
    case "12":
        genre = "category/books/religion_12/"
    case "13":
        genre = "category/books/nonfiction_13/"
    case "14":
        genre = "category/books/music_14/"
    case "15":
        genre = "category/books/default_15/"
    case "16":
        genre = "category/books/science-fiction_16/"
    case "17":
        genre = "category/books/sports-and-games_17/"
    case "18":
        genre = "category/books/add-a-comment_18/"
    case "19":
        genre = "category/books/fantasy_19/"
    case "20":
        genre = "category/books/new-adult_20/"
    case "21":
        genre = "category/books/young-adult_21/"
    case "22":
        genre = "category/books/science_22/"
    case "23":
        genre = "category/books/poetry_23/"
    case "24":
        genre = "category/books/paranormal_24/"
    case "25":
        genre = "category/books/art_25/"
    case "26":
        genre = "category/books/psychology_26/"
    case "27":
        genre = "category/books/autobiography_27/"
    case "28":
        genre = "category/books/parenting_28/"
    case "29":
        genre = "category/books/adult-fiction_29/"
    case "30":
        genre = "category/books/humor_30/"
    case "31":
        genre = "category/books/horror_31/"
    case "32":
        genre = "category/books/history_32/"
    case "33":
        genre = "category/books/food-and-drink_33/"
    case "34":
        genre = "category/books/christian-fiction_34/"
    case "35":
        genre = "category/books/business_35/"
    case "36":
        genre = "category/books/biography_36/"
    case "37":
        genre = "category/books/thriller_37/"
    case "38":
        genre = "category/books/contemporary_38/"
    case "39":
        genre = "category/books/spirituality_39/"
    case "40":
        genre = "category/books/academic_40/"
    case "41":
        genre = "category/books/self-help_41/"
    case "42":
        genre = "category/books/historical_42/"
    case "43":
        genre = "category/books/christian_43/"
    case "44":
        genre = "category/books/suspense_44/"
    case "45":
        genre = "category/books/short-stories_45/"
    case "46":
        genre = "category/books/novels_46/"
    case "47":
        genre = "category/books/health_47/"
    case "48":
        genre = "catalogue/category/books/politics_48/"
    case "49":
        genre = "category/books/cultural_49/"
    case "50":
        genre = "catalogue/category/books/erotica_50/"
    case "51":
        genre = "category/books/crime_51/"
    case _:
        genre = "catagory/books_1/"

getAllLinksBook(BASE_URL + genre + "index.html")



for link in links:
    link.split('/')
    scrapPage(BASE_URL + link.split('/')[3])


print(len(links))