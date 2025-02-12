from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

from parser import parse_product

url = "https://ksize.ru/shtatnaya-magnitola-bmw-3-f30-f31-f34-f35-f80-2011-2019-wide-media-ks2125qr-4-32-nbt-00000027666.html"
product = parse_product(url)
print(product)