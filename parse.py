from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

from parser import parse_caregory

url = "https://ksize.ru/shtatnye-golovnye-ustroystva-dlya-audi"

parse_caregory(url)
logging.info("Parsing completed")