"""
This module provides functionality to scrape data from a single product page and store it in a CSV file. (This will typically not be used if scraping multiple items.)

Example usage:
    config = Config(debug_mode=True)
    product_data = scrape_one_product('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', config)

Modules Required:
    - requests
    - bs4 (BeautifulSoup)
    - util (url_to_soup, extract_product_info, write_product_to_csv)
    - os
    - csv

Scraped data format:
    - Product Title
    - Product Description
    - Product Information (e.g., UPC, Product Type, Genre, Prices, Tax, Availability, Number of reviews, URL)
"""

from util import url_to_soup, extract_product_info, write_product_to_csv
import requests
from bs4 import BeautifulSoup
import sys
import csv
import os


def scrape_one_product(url, config):
    """
    Scrapes data for a single product from the given URL and writes it to a CSV file.

    Args:
        url (str): The URL of the product page to scrape.
        config (Config): An instance of the `Config` class, specifying options like debug and demo modes.

    Returns:
        dict: A dictionary of the product information if successful, or None if scraping failed.
    """

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