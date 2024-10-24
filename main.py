import sys
import logging

from one_product import scrape_one_product
from one_category import scrape_one_category
from all_categories import scrape_whole_site


class Config:
    def __init__(self, debug_mode=False, demo_mode=False, scraping_images=True):
        self.DEBUG_MODE = debug_mode
        self.DEMO_MODE = demo_mode
        self.SCRAPING_IMAGES = scraping_images

def main() -> int:
    print("Starting scrape.")

    config = Config(debug_mode=False, demo_mode=False, scraping_images=True)

    #product = scrape_one_product('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', config)
    #products_from_category = scrape_one_category('https://books.toscrape.com/catalogue/category/books/mystery_3/index.html', config)
    #complete = scrape_whole_site(config)
    all_with_imgs = scrape_whole_site(config) 

    print("Finished scraping.")

    return 0

if __name__ == '__main__':
    sys.exit(main())
