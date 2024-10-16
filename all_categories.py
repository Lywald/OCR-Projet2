import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import csv
import time
import os

from one_category import scrape_one_category


# Specify the directory path
directory_path = "csv"
# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)

def scrape_whole_site():
    base_URL = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
    category_url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
    urlPage = 0
    url = 'none'

    categURLs = []

    responseCategory = requests.get(base_URL)
    categSoup = BeautifulSoup(responseCategory.text, 'lxml')
    categNav = categSoup.find("ul", {"class":"nav-list"})
    categHrefs = categNav.findAll("a")[1:]


    for categ in categHrefs:
        categURLs.append(urljoin(base_URL, categ["href"]))

    print(str(categURLs))

for categURL in categURLs:
    scrape_one_category(categURL)

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