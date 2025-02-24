import logging
from csv import DictWriter
from .products import Product

def write_products_csv(products: list[Product], file_name: str) -> None:
    headers = []
    for product in products:
        keys = list(product.model_dump().keys())
        if len(keys) > len(headers):
            headers = keys
    with open(f"{file_name}.csv", "w", newline="") as file:
        writer = DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for product in products:
            writer.writerow(product.model_dump())
    logging.info("CSV file written successfully")