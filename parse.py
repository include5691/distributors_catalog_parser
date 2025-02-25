from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)

import os
from parser import parse_subcategory

parse_subcategory(os.getenv("SUBCATEGORY_URL"), os.getenv("CATEGORIES_PATH"))
logging.info("Parsing completed")