from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)

import os
from src.process import process_subcategories
from .parser import get_subcategories_urls, get_products

url = os.getenv("SUBCATEGORY_URL")
subcategories = get_subcategories_urls(url)
if not subcategories:
    logging.error(f"Subcategories not found for url {url}")
    exit
process_subcategories(subcategories)
logging.info("Parsing completed")