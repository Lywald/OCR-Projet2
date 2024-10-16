import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import csv
import time
import os

# Specify the directory path
directory_path = "csv"
# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)

# Specify the directory path
directory_path = "images"
# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)

urlBase = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
urlCat = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
urlPage = 0
url = 'none'

categURLs = []

responseCategory = requests.get(urlBase)
categSoup = BeautifulSoup(responseCategory.text, 'lxml')
categNav = categSoup.find("ul", {"class":"nav-list"})
categHrefs = categNav.findAll("a")[1:]


for categ in categHrefs:
    categURLs.append(urljoin(urlBase, categ["href"]))

print(str(categURLs))

for categURL in categURLs:
    urlCat = categURL
    if "category" in urlCat:
        categoryName = urlCat.split('/')[-2]
        with open(f"{categoryName}.csv", "w", newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["ProductTitle", "ProductDescription", "UPC", "ProductType", "PriceExclTax", "PriceInclTax", "Tax", "Availability", "NumberOfReviews", "StarRating"])
            response = requests.get(urlCat)
            while response.ok:
                catSoup = BeautifulSoup(response.text, 'lxml')
                booksPods = catSoup.findAll("article")
                for bookPod in booksPods:
                    time.sleep(0.1)
                    bookUrl = urljoin(urlCat, bookPod.find("a")["href"])
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

                        picURL = soup.find("img")["src"]
                        picFullURL = urljoin(bookUrl, picURL)
                        picDL = requests.get(picFullURL)
                        if picDL.status_code == 200:
                            print("Image downloaded successfully!")
                            with open(f"images/{infoUPC.text}.jpg", "wb") as imgFile:
                                imgFile.write(picDL.content)
                        else:
                            print("Failed to download image.")
                        ############################# Write all information into CSV #################################
                        writer.writerow([productTitle.text, productDescription.text, infoUPC.text, infoProductType.text, infoPriceExclTax.text[1:], infoPriceInclTax.text[1:], infoTax.text[1:], infoAvailability.text, infoReviews.text, infoStarRating])
                hasNextPage = catSoup.find("li", {"class": "next"})
                if hasNextPage is not None:
                    nextA = hasNextPage.find('a')["href"]
                    absoluteNextUrl = urljoin(urlCat, nextA)
                    print("Absolute Next URL : " + absoluteNextUrl)
                    response = requests.get(absoluteNextUrl)
                else:
                    break



