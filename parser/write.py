import logging
from csv import DictWriter
from .products import Product

def write_csv(products: list[Product]) -> None:
    with open("products.csv", "w", newline="") as file:
        writer = DictWriter(file, fieldnames=["Name", "Short description", "Images"])
        writer.writeheader()
        for product in products:
            writer.writerow(product.model_dump())
    logging.info("CSV file written successfully")