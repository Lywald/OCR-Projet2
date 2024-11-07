"""
main.py

This script serves as the entry point for the web scraping project. It orchestrates the data extraction. 

Modules:
- `all_categories.py`: Collects data from all target categories and organizes scraping tasks.
- `one_category.py`: Focuses on extracting data within a single category.
- `one_product.py`: Scrapes individual product data, enriching the dataset with specific details.

Usage:
Run this script to start the full data scraping pipeline. The results are saved as a CSV file.

Example:
    python main.py
"""

import sys
import logging

from one_product import scrape_one_product
from one_category import scrape_one_category
from all_categories import scrape_whole_site


class Config:
    """
    Configuration settings for the web scraping project.

    Attributes:
        DEBUG_MODE (bool): If True, enables debug-level logging and detailed error messages.
        DEMO_MODE (bool): If True, limits the scraping process for demonstration purposes.
        SCRAPING_IMAGES (bool): If True, enables image scraping as part of the data extraction.
    """

    def __init__(self, debug_mode=False, demo_mode=False, scraping_images=True):
        self.DEBUG_MODE = debug_mode
        self.DEMO_MODE = demo_mode
        self.SCRAPING_IMAGES = scraping_images

def main() -> int:
    """
    The main entry point for starting the web scraping process.

    This function initializes the configuration for the scraping session, then proceeds to scrape
    the entire site using the specified settings. It includes options to scrape individual products 
    or categories, (though they are currently commented out). By default, it configures `demo_mode` 
    to limit the scraping scope and enables image scraping.

    Returns:
        int: Exit status code, where 0 indicates successful execution.
    """
    
    print("Starting scrape.")

    config = Config(debug_mode=False, demo_mode=True, scraping_images=True)

    #product = scrape_one_product('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', config)
    #products_from_category = scrape_one_category('https://books.toscrape.com/catalogue/category/books/mystery_3/index.html', config)
    #complete = scrape_whole_site(config)
    all_with_imgs = scrape_whole_site(config) 

    print("Finished scraping.")

    return 0

if __name__ == '__main__':
    sys.exit(main())
