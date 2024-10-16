import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import csv
import time
import os

from one_category import scrape_one_category
from util import url_to_soup

directory_path = "csv"
# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)
os.makedirs("images", exist_ok=True)

def scrape_whole_site(scrape_images=False):
    base_URL = 'https://books.toscrape.com/catalogue/category/books_1/index.html'
    category_url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

    categories_URLs = []

    front_page_soup = url_to_soup(base_URL)  # Extracting the list of genres
    categories_navigation_panel = front_page_soup.find("ul", {"class":"nav-list"})
    categories_hrefs = categories_navigation_panel.findAll("a")[1:]

    for category in categories_hrefs:
        categories_URLs.append(urljoin(base_URL, category["href"]))

    print(str(categories_URLs))

    for category_URL in categories_URLs:
        scrape_one_category(category_URL, scrape_images) # Scrape all genres