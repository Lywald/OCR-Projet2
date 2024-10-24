"""
Scraped data:


Product Title

Product Description

Product Information
    UPC	=> a897fe39b1053632
    Product Type =>	Books
    Genre => Mystery
    Price (excl. tax) =>	£51.77
    Price (incl. tax) =>	£51.77
    Tax	=> £0.00
    Availability =>	In stock (22 available)
    Number of reviews =>	0
    URL => https://books.toscrape.com/catalogue/ways-of-seeing_94/index.html

"""

from util import url_to_soup, extract_product_info, write_product_to_csv
import requests
from bs4 import BeautifulSoup
import sys
import csv
import os


def scrape_one_product(url, config):
    directory_path = "csv"
    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)

    soup = url_to_soup(url, config)
    if soup is not None:
        product_infos = extract_product_info(soup, url, config)
        if config.DEBUG_MODE:
            print(product_infos)
        write_product_to_csv(f"csv/books/{product_infos['UPC']}.csv", product_infos, "w")
        return product_infos
    return None