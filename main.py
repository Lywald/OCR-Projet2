import sys

from one_product import scrape_one_product
from one_category import scrape_one_category
from all_categories import scrape_whole_site

def main() -> int:
    #product = scrape_one_product()
    #products_from_category = scrape_one_category()
    complete = scrape_whole_site()

    return 0

if __name__ == '__main__':
    sys.exit(main())
