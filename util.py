"""
Utilities for scraping and saving product and category data as CSV files.

Functions:
- `url_to_soup`: Fetches HTML from a URL and converts it to a BeautifulSoup object.
- `extract_product_info`: Extracts product details like title, price, and availability.
- `extract_category`: Scrapes all products in a category and saves them as a list of dictionaries.
- `write_product_to_csv`: Saves a single product's data to a CSV file.
- `write_category_to_csv`: Saves an entire category's products to a CSV file.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import sys
import csv
import os

def url_to_soup(url, config):
    """
    Fetches the HTML content of a URL and converts it to a BeautifulSoup object.

    Args:
        url (str): The URL of the page to scrape.
        config (Config): Configuration for debugging and demo mode.

    Returns:
        BeautifulSoup: Parsed HTML content if successful, or None if failed.
    """

    response = requests.get(url)
    if response.ok:
        if config.DEBUG_MODE:
            print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    return None

def extract_product_info(soup, book_url, config):
    """
    Extracts details of a product (title, description, price, etc.) from a soup object.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the product page.
        book_url (str): URL of the product.
        config (Config): Configuration for debugging and image scraping.

    Returns:
        dict: A dictionary with extracted product details.
    """

    product_title = soup.find("div", {"class": "product_main"}).find("h1").text
    product_description = soup.findAll("p")[3].text
    product_genre = soup.findAll("li")[2].find("a").text

    info_body_TRs = soup.find("table").findAll("td")

    info_UPC = info_body_TRs[0].text
    info_product_type = info_body_TRs[1].text
    info_price_excltax = info_body_TRs[2].text[1:]
    info_price_incltax = info_body_TRs[3].text[1:]
    info_tax = info_body_TRs[4].text[1:]
    info_availability = info_body_TRs[5].text
    info_reviews = info_body_TRs[6].text
    info_star_rating = soup.find("p", {"class": "star-rating"}).get('class')[1]

    if config.SCRAPING_IMAGES:
        pic_URL = soup.find("img")["src"]
        pic_full_URL = urljoin(book_url, pic_URL)
        pic_DL = requests.get(pic_full_URL)
        if pic_DL.status_code == 200:
            if config.DEBUG_MODE:
                print("Image downloaded successfully!")
            with open(f"images/{info_UPC}.jpg", "wb") as img_file:
                img_file.write(pic_DL.content)
        else:
            if config.DEBUG_MODE:
                print("Failed to download image.")

    return {
        "product_title": product_title,
        "product_description": product_description,
        "UPC": info_UPC,
        "product_genre": product_genre,
        "ProductType": info_product_type,
        "PriceExclTax": info_price_excltax,
        "PriceInclTax": info_price_incltax,
        "Tax": info_tax,
        "Availability": info_availability,
        "NumberOfReviews": info_reviews,
        "StarRating": info_star_rating,
        "URL": book_url
    }

def extract_category(category_name, category_url, category_soup, config):
    """
    Scrapes all products in a given category and returns them as a list of dictionaries.

    Args:
        category_name (str): Name of the category.
        category_url (str): URL of the category page.
        category_soup (BeautifulSoup): Parsed HTML of the category page.
        config (Config): Configuration settings for scraping.

    Returns:
        list of dict: List of product information dictionaries.
    """

    book_list = []
    booksProcessedQuantity = 0

    with open(f"csv/categories/{category_name}.csv", "w", newline='', encoding='utf-8') as csvFile:
        response = requests.get(category_url)
        while response.ok:
            #category_soup = BeautifulSoup(response.text, 'lxml')
            books_pods = category_soup.findAll("article")
            for book_pod in books_pods:
                time.sleep(0.3)
                book_url = urljoin(category_url, book_pod.find("a")["href"])
                #response_book = requests.get(book_url)
                book_soup = url_to_soup(book_url, config)
                if book_soup is not None:
                    latest_book_infos = extract_product_info(book_soup, book_url, config)
                    book_list.append(latest_book_infos)
                    if config.DEBUG_MODE:
                        print(book_url + "\n")
                    booksProcessedQuantity += 1
                    print("Processed " + str(booksProcessedQuantity) + " from category: " + category_name)

                    if config.DEMO_MODE and booksProcessedQuantity >= 5:
                        break # Scraping maximum 5 books in Demo Mode
                    
            has_next_page = category_soup.find("li", {"class": "next"})
            if has_next_page is not None:
                next_A = has_next_page.find('a')["href"]
                absolute_next_URL = urljoin(category_url, next_A)
                if config.DEBUG_MODE:
                    print("Absolute Next URL : " + absolute_next_URL)
                response = requests.get(absolute_next_URL)
                category_soup = url_to_soup(absolute_next_URL, config)
            else:
                break

        return book_list


def write_product_to_csv(file_path, product_info, write_mode = "w"):
    """
    Writes a single product's information to a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        product_info (dict): Product data to write.
        write_mode (str): File write mode, default is "w".
    """

    with open(file_path, write_mode, newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([
            "Product Title", "Product Description", "UPC", "Genre",
            "Product Type", "Price Excl. Tax", "Price Incl. Tax", 
            "Tax", "Availability", "Number Of Reviews", "Star Rating", "URL"
        ])
        writer.writerow([
            product_info["product_title"], product_info["product_description"], 
            product_info["UPC"], product_info["product_genre"], 
            product_info["ProductType"], product_info["PriceExclTax"], 
            product_info["PriceInclTax"], product_info["Tax"], 
            product_info["Availability"], product_info["NumberOfReviews"], 
            product_info["StarRating"], product_info["URL"]
        ])

def write_category_to_csv(category_path, category_books, write_mode = "w"):
    """
    Writes a list of products in a category to a CSV file.

    Args:
        category_path (str): Path to the CSV file.
        category_books (list of dict): List of product data dictionaries.
        write_mode (str): File write mode, default is "w".
    """

    with open(category_path, write_mode, newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([
            "Product Title", "Product Description", "UPC", "Genre",
            "Product Type", "Price Excl. Tax", "Price Incl. Tax", 
            "Tax", "Availability", "Number Of Reviews", "Star Rating", "URL"
        ])
        for product_info in category_books:
            writer.writerow([
                        product_info["product_title"], product_info["product_description"], 
                        product_info["UPC"], product_info["product_genre"], 
                        product_info["ProductType"], product_info["PriceExclTax"], 
                        product_info["PriceInclTax"], product_info["Tax"], 
                        product_info["Availability"], product_info["NumberOfReviews"], 
                        product_info["StarRating"], product_info["URL"]
                    ])    