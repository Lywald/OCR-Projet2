import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import csv
import time
import os

from one_category import scrape_one_category
from util import url_to_soup

# Specify the directory path
directory_path = "csv"
# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)
os.makedirs("images", exist_ok=True)

def scrape_whole_site(scrape_images=False):
    base_URL = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
    category_url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
    urlPage = 0
    url = 'none'

    categories_URLs = []

    front_page_response = requests.get(base_URL)
    front_page_soup = BeautifulSoup(front_page_response.text, 'lxml')
    categories_navigation_panel = front_page_soup.find("ul", {"class":"nav-list"})
    categories_hrefs = categories_navigation_panel.findAll("a")[1:]

    for category in categories_hrefs:
        categories_URLs.append(urljoin(base_URL, category["href"]))

    print(str(categories_URLs))

    for category_URL in categories_URLs:
        scrape_one_category(category_URL, scrape_images)


"""for categURL in categURLs:
    category_url = categURL
    if "category" in category_url:
        categoryName = category_url.split('/')[-2]
        with open(f"{categoryName}.csv", "w", newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["ProductTitle", "ProductDescription", "UPC", "ProductType", "PriceExclTax", "PriceInclTax", "Tax", "Availability", "NumberOfReviews", "StarRating"])
            response = requests.get(category_url)
            while response.ok:
                catSoup = BeautifulSoup(response.text, 'lxml')
                booksPods = catSoup.findAll("article")
                for bookPod in booksPods:
                    time.sleep(0.1)
                    bookUrl = urljoin(category_url, bookPod.find("a")["href"])
                    responseBook = requests.get(bookUrl)
                    #print(responseBook.text)
                    if responseBook.ok:
                        #print(response.text)
                        soup = BeautifulSoup(responseBook.text, 'lxml')
                        csvPath = soup.find("table").find("td").text #use UPC as csv filename
                        ################################ Extract all informations ####################################
                        productTitle = soup.find("div", {"class": "product_main"}).find("h1")
                        print("Product Title: ")
                        print(productTitle.text)
                        #csvFile.write(productTitle)

                        productDescription = soup.findAll("p")[3]
                        print("Product Description")
                        print(productDescription.text)

                        print("Product Information:")
                        infoBody = soup.find("table")
                        
                        infoBodyTRs =  infoBody.findAll("td")
                        [print(infoB.text) for infoB in infoBodyTRs]

                        infoUPC = infoBodyTRs[0]
                        infoProductType = infoBodyTRs[1]
                        infoPriceExclTax = infoBodyTRs[2]
                        infoPriceInclTax = infoBodyTRs[3]
                        infoTax = infoBodyTRs[4]
                        infoAvailability = infoBodyTRs[5]
                        infoReviews = infoBodyTRs[6]

                        infoStarRating = soup.find("p", {"class": "star-rating"}).get('class')[1]
                        print(infoStarRating)
                        ############################# Write all information into CSV #################################
                        writer.writerow([productTitle.text, productDescription.text, infoUPC.text, infoProductType.text, infoPriceExclTax.text[1:], infoPriceInclTax.text[1:], infoTax.text[1:], infoAvailability.text, infoReviews.text, infoStarRating])
                hasNextPage = catSoup.find("li", {"class": "next"})
                if hasNextPage is not None:
                    nextA = hasNextPage.find('a')["href"]
                    absoluteNextUrl = urljoin(category_url, nextA)
                    print("Absolute Next URL : " + absoluteNextUrl)
                    response = requests.get(absoluteNextUrl)
                else:
                    break



"""