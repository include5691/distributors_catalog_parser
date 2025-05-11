import os
import logging
from pathlib import Path
from urllib.parse import urlparse
from ._write import write_products_csv


def process_subcategory(url: str, categories_path: str, get_products_func: callable):
    logging.info(f"Parsing subcategory {url}")
    products = get_products_func(url, categories_path)
    if not products:
        logging.error(f"Products not found for url {url}")
        return None
    dir_path = _get_dir_path(url)
    if not dir_path.exists():
        dir_path.mkdir(parents=True)
    for i, product in enumerate(products):
        write_products_csv(
            [product], file_name=str(dir_path) + f"/{dir_path.name}_{i}.csv"
        )
    logging.info(f"Subcategory {url} parsed")


def _get_dir_path(url: str) -> Path:
    parsed_url = urlparse(url)
    return Path(
        str(Path(__file__).parent / "csv_files")
        + f"/{parsed_url.path.split("dlya")[-1][1:]}"
    )


def process_subcategories(subcategories: list, get_products_func: callable):
    for subcategory in subcategories:
        dir_path = _get_dir_path(subcategory)
        if not dir_path.exists():
            car_category_name = dir_path.name.replace("-", " ").strip()
            process_subcategory(
                subcategory,
                categories_path=os.getenv("CATEGORIES_PATH").format(
                    car_category_name=car_category_name.upper()
                ),
                get_products_func=get_products_func,
            )
