import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import csv
import time
import os

from util import url_to_soup, extract_product_info, extract_category, write_category_to_csv

# Specify the directory path
directory_path = "csv"
# Create the directories if they don't exist
os.makedirs(directory_path, exist_ok=True)
os.makedirs(directory_path + "/books", exist_ok=True)
os.makedirs(directory_path + "/categories", exist_ok=True)

def scrape_one_category(category_url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"):
    if "category" in category_url:
        url_page = 0
        category_soup = url_to_soup(category_url)
        
        if category_soup is not None:
            category_name = category_url.split('/')[-2]
            category_books = extract_category(category_name, 
                                              category_url, 
                                              category_soup)
            print(category_books)
            write_category_to_csv(f"csv/categories/{category_name}.csv", 
                                    category_books, "w")
            return category_books
        return None

        


