from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)

from parser import parse_subcategory

url = "https://ksize.ru/shtatnye-golovnye-ustroystva-dlya-audi"
categories = "Автомагнитолы > Штатные автомагнитолы > Автомагнитолы Audi"

parse_subcategory(url, categories)
logging.info("Parsing completed")