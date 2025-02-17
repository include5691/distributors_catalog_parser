import logging
from bs4 import BeautifulSoup
from ._product import Product
from ._html import get_html
from ._common import KSIZE_URL

def get_product(url: str) -> Product | None:
    html_content = get_html(url)
    if html_content is None:
        return None
    soup = BeautifulSoup(html_content, "html.parser")
    title_tag = soup.find("h1")
    if not title_tag:
        logging.error(f"Title not found for url {url}")
    name = title_tag.get_text(strip=True)
    short_description = None
    short_description_tag = soup.find("div", itemprop="description")
    if short_description_tag:
        short_description = short_description_tag.get_text(strip=True)
    images = []
    product_items = soup.find_all("div", class_="s-nomenclature__photo-item")
    for item in product_items:
        img_tag = item.find("img")
        if img_tag:
            images.append(KSIZE_URL + img_tag["src"])
    return Product(name=name, short_description=short_description, images=images)