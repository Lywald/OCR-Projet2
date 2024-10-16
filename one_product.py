"""
Scraped data:


Product Title

Product Description

Product Information
    UPC	=> a897fe39b1053632
    Product Type =>	Books
    Price (excl. tax) =>	£51.77
    Price (incl. tax) =>	£51.77
    Tax	=> £0.00
    Availability =>	In stock (22 available)
    Number of reviews =>	0


"""

from util import url_to_soup, extract_product_info, write_product_to_csv
import requests
from bs4 import BeautifulSoup
import sys
import csv
import os

# Specify the directory path
directory_path = "csv"
# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)

def scrape_one_product(url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'):
    if len(sys.argv) > 1: # optionnally provide a book's link as argument
        print(sys.argv[1])
        url = sys.argv[1]

    soup = url_to_soup(url)

    if soup is not None:
        product_infos = extract_product_info(soup)
        print(product_infos)
        write_product_to_csv(f"csv/books/{product_infos['UPC']}.csv", product_infos, "w")
        return product_infos
        
    return None






    """if soup is not None:
        csv_path = soup.find("table").find("td").text #use UPC as csv filename

        with open(f"{csv_path}.csv", "w", newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["product_title", "product_description", "UPC", 
                            "ProductType", "PriceExclTax", "PriceInclTax", "Tax", 
                            "Availability", "NumberOfReviews", "StarRating"])
            ################################ Extract all informations ############
            product_title = soup.find("div", {"class": "product_main"}).find("h1")
            print("Product Title: ")
            print(product_title.text)
            #csvFile.write(product_title)

            product_description = soup.findAll("p")[3]
            print("Product Description")
            print(product_description.text)

            print("Product Information:")
            info_body = soup.find("table")
            
            info_body_TRs =  info_body.findAll("td")
            [print(info_TR.text) for info_TR in info_body_TRs]

            info_UFC = info_body_TRs[0]
            info_product_type = info_body_TRs[1]
            info_price_excltax = info_body_TRs[2]
            info_price_incltax = info_body_TRs[3]
            info_tax = info_body_TRs[4]
            info_availability = info_body_TRs[5]
            info_reviews = info_body_TRs[6]

            info_star_rating = soup.find("p", {"class": "star-rating"}).get('class')[1]
            print(info_star_rating.text)
            ############################# Write all information into CSV #########
            writer.writerow([product_title.text, product_description.text, 
                            info_UFC.text, info_product_type.text, 
                            info_price_excltax.text[1:], 
                            info_price_incltax.text[1:],
                            info_tax.text[1:], info_availability.text, 
                            info_reviews.text, info_star_rating.text])
        

"""