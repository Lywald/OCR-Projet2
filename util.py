import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
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

def extract_product_info(soup, book_url, scrape_images=False):
    """Extracts product information from the soup object."""
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

    if (scrape_images):
        picURL = soup.find("img")["src"]
        picFullURL = urljoin(book_url, picURL)
        picDL = requests.get(picFullURL)
        if picDL.status_code == 200:
            print("Image downloaded successfully!")
            with open(f"images/{info_UPC}.jpg", "wb") as imgFile:
                imgFile.write(picDL.content)
        else:
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

def extract_category(category_name, category_url, category_soup, scrape_images=False):
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
                book_soup = url_to_soup(book_url)
                if book_soup is not None:
                    latest_book_infos = extract_product_info(book_soup, book_url, scrape_images)
                    book_list.append(latest_book_infos)
                    print(book_url + "\n")
                    booksProcessedQuantity += 1
                    print("Processed " + str(booksProcessedQuantity) + " from category: " + category_name)
                    
            has_next_page = category_soup.find("li", {"class": "next"})
            if has_next_page is not None:
                next_A = has_next_page.find('a')["href"]
                absolute_next_URL = urljoin(category_url, next_A)
                print("Absolute Next URL : " + absolute_next_URL)
                response = requests.get(absolute_next_URL)
                category_soup = url_to_soup(absolute_next_URL)
            else:
                break

        return book_list


def write_product_to_csv(file_path, product_info, write_mode = "w"):
    """Writes product information to a CSV file."""
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



    