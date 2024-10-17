# OCR-Projet2
Scraping of http://books.toscrape.com/
OpenClassRooms Project 2

# Description

We convert this website's books data into CSV files with the following columns:
"Product Title", "Product Description", "UPC", "Genre",
"Product Type", "Price Excl. Tax", "Price Incl. Tax", 
"Tax", "Availability", "Number Of Reviews", "Star Rating", "URL"

The code is launched with the command:
python -m main

Each script builds on the previous, and each script uses imported util.py utilitary functions. 

The output is located in "csv" and "images" subfolders.

# Project structure

main.py
|__ main()

one_product.py
|__ scrape_one_product

one_category.py
|__ scrape_one_category

all_categories.py
|__ scrape_whole_site

util.py
|__ url_to_soup
|__ extract_product_info
|__ extract_category
|__ write_product_to_csv
|__ write_category_to_csv
