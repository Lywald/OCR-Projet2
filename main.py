import sys

from one_product import scrape_one_product

def main() -> int:
    product = scrape_one_product()
    return 0

if __name__ == '__main__':
    sys.exit(main())
