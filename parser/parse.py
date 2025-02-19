import logging
from .categories import get_subcategories
from .products import get_products
from .write import write_csv

def parse_caregory(url: str):
    subcategories = get_subcategories(url)
    if not subcategories:
        logging.error(f"Subcategories not found for url {url}")
        return None
    products = []
    for subcategory in subcategories:
        print(subcategory)
        result = get_products(subcategory)
        if result:
            products.extend(result)
    if not products:
        logging.error(f"Products not found for url {url}")
        return None
    write_csv(products)
    logging.info(f"Category {url} parsed successfully")