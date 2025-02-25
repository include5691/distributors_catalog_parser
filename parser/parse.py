import logging
from urllib.parse import urlparse
from .categories import get_subcategories_urls
from .products import get_products
from .write import write_products_csv

def parse_caregory(url: str):
    subcategories = get_subcategories_urls(url)
    if not subcategories:
        logging.error(f"Subcategories not found for url {url}")
        return None
    products = []
    for subcategory in subcategories:
        parse_subcategory(subcategory)

def parse_subcategory(url: str, categories_path: str | None = None):
    products = get_products(url, categories_path)
    if not products:
        logging.error(f"Products not found for url {url}")
        return None
    parsed_url = urlparse(url)
    for n in range(len(products) // 20 + 1):
        write_products_csv(products[n*20:(n+1)*20], file_name=parsed_url.path.replace("/", "") + f"_{n}")