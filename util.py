import requests
from bs4 import BeautifulSoup
import sys
import csv
import os

def url_to_soup(url):
    response = requests.get(url)

    if response.ok:
        print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    return None

def scrape_book_data(soup):
    return

def extract_product_info(soup):
    """Extracts product information from the soup object."""
    product_title = soup.find("div", {"class": "product_main"}).find("h1").text
    product_description = soup.findAll("p")[3].text
    info_body_TRs = soup.find("table").findAll("td")

    info_UPC = info_body_TRs[0].text
    info_product_type = info_body_TRs[1].text
    info_price_excltax = info_body_TRs[2].text[1:]
    info_price_incltax = info_body_TRs[3].text[1:]
    info_tax = info_body_TRs[4].text[1:]
    info_availability = info_body_TRs[5].text
    info_reviews = info_body_TRs[6].text
    info_star_rating = soup.find("p", {"class": "star-rating"}).get('class')[1]

    return {
        "product_title": product_title,
        "product_description": product_description,
        "UPC": info_UPC,
        "ProductType": info_product_type,
        "PriceExclTax": info_price_excltax,
        "PriceInclTax": info_price_incltax,
        "Tax": info_tax,
        "Availability": info_availability,
        "NumberOfReviews": info_reviews,
        "StarRating": info_star_rating
    }

def write_product_to_csv(file_path, product_info, write_mode = "w"):
    """Writes product information to a CSV file."""
    with open(file_path, write_mode, newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([
            "product_title", "product_description", "UPC", 
            "ProductType", "PriceExclTax", "PriceInclTax", 
            "Tax", "Availability", "NumberOfReviews", "StarRating"
        ])
        writer.writerow([
            product_info["product_title"], product_info["product_description"], 
            product_info["UPC"], product_info["ProductType"],
            product_info["PriceExclTax"], product_info["PriceInclTax"],
            product_info["Tax"], product_info["Availability"], 
            product_info["NumberOfReviews"], product_info["StarRating"]
        ])