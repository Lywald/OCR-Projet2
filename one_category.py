"""
This module provides functionality to scrape multiple products from a single product category page and store it in a CSV file.

Example usage:
    config = Config(debug_mode=True)
    category_data = scrape_one_category('https://books.toscrape.com/catalogue/category/books/mystery_3/index.html', config)

Scraped data format:
    - Product Title
    - Product Description
    - Product Information (e.g., UPC, Product Type, Genre, Prices, Tax, Availability, Number of reviews, URL)
    - Stored in CSV files organized by category.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import csv
import time
import os

from util import url_to_soup, extract_product_info, extract_category, write_category_to_csv


def scrape_one_category(category_url, config):
    """
    Scrapes data for all products in a specified category and writes it to a CSV file.

    This function navigates to the provided category URL, extracts all product details on the page, 
    such as title, pricing, stock availability, and metadata, and stores the data in a CSV file. 
    The filename is based on the category name, and files are saved in the 'csv/categories/' directory. 
    If `DEBUG_MODE` is enabled in the `Config` instance, the extracted data is printed to the console.

    Returns:
        list of dict: A list of dictionaries containing product information for all items in the category, 
                      or None if scraping failed.
    """
    
    directory_path = "csv"
    # Create the directories if they don't exist
    os.makedirs(directory_path, exist_ok=True)
    os.makedirs(directory_path + "/books", exist_ok=True)
    os.makedirs(directory_path + "/categories", exist_ok=True)

    if "category" in category_url:
        category_soup = url_to_soup(category_url, config)        
        if category_soup is not None:
            category_name = category_url.split('/')[-2]
            category_books = extract_category(category_name, 
                                              category_url, 
                                              category_soup, config)
            if config.DEBUG_MODE:
                print(category_books)
            write_category_to_csv(f"csv/categories/{category_name}.csv", 
                                    category_books, "w")
            return category_books
    return None

        


