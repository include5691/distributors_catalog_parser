from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)

import os
from src.ksize.parser import process_caregory

process_caregory(os.getenv("SUBCATEGORY_URL"))
logging.info("Parsing completed")