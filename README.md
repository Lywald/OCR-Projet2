# OCR-Projet2
Scraping of http://books.toscrape.com/

OpenClassRooms Project 2

# Description

We convert this website's books data into CSV files with the following columns:

*"Product Title", "Product Description", "UPC", "Genre",*
*"Product Type", "Price Excl. Tax", "Price Incl. Tax", *
*"Tax", "Availability", "Number Of Reviews", "Star Rating", "URL"*

The project is launched with the commands:

1. *pip install virtualenv*

2. *virtualenv bookscraping*

3. *bookscraping\Scripts\activate*

4. *pip install -r requirements.txt*

5. *python -m main*

6. *deactivate*

Each script builds on the previous, and each script uses imported util.py utilitary functions. 

The output is located in "csv" and "images" subfolders. 

# Project structure

main.py  
├── main()

one_product.py  
├── scrape_one_product

one_category.py  
├── scrape_one_category

all_categories.py  
├── scrape_whole_site

util.py  
├── url_to_soup  
├── extract_product_info  
├── extract_category  
├── write_product_to_csv  
└── write_category_to_csv
