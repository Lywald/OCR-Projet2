"""
This module provides functionality to scrape data from all product categories on the site and store it in organized CSV files.

The module navigates through the homepage to gather URLs for each category, then scrapes each category individually using 
the `scrape_one_category` function. The scraped data, including details like title, description, price, and availability, 
is stored as CSV files in dedicated folders. Images can also be scraped and saved if enabled in the configuration.

Example usage:
    config = Config(debug_mode=True, demo_mode=False, scraping_images=True)
    scrape_whole_site(config)
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import csv
import time
import os

from one_category import scrape_one_category
from util import url_to_soup


def scrape_whole_site(config):
    """
    Scrapes data for all product categories on the site and saves them in CSV files.

    This function navigates to the site’s homepage, extracts all category URLs, and iterates over them to 
    scrape each category individually using `scrape_one_category`. The data collected from each category 
    includes product details like title, price, and stock availability. CSV files for each category are saved 
    in the 'csv/categories/' directory, and images are saved in the 'images' directory if `scraping_images` 
    is enabled in the configuration. In `DEMO_MODE`, the scraping process is limited to a single category.
    """
    
    directory_path = "csv"
    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)
    os.makedirs("images", exist_ok=True)

    base_URL = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
    category_url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

    categories_URLs = []

    front_page_soup = url_to_soup(base_URL, config)  # Extracting the list of genres
    categories_navigation_panel = front_page_soup.find("ul", {"class":"nav-list"})
    categories_hrefs = categories_navigation_panel.findAll("a")[1:]

    for category in categories_hrefs:
        categories_URLs.append(urljoin(base_URL, category["href"]))

    if config.DEBUG_MODE:
        print(str(categories_URLs))

    for category_URL in categories_URLs:
        scrape_one_category(category_URL, config) # Scrape all genres
        if config.DEMO_MODE:
            break # Stop at first category in Demo Mode
