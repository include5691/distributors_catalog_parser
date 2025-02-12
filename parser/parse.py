import os
import logging
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from ._product import Product

def _get_html_content(url: str) -> str | None:
    try:
        with requests.Session() as session:
            response = session.get(url)
            if response.status_code == 200:
                return response.text
    except RequestException as e:
        logging.error(f"Request error: {e}")

def parse_product(url: str) -> Product | None:
    html_content = _get_html_content(url)
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

    product_items = soup.find_all("div", class_="s-nomenclature__photo-item")
    images = []
    product_items = soup.find_all("div", class_="s-nomenclature__photo-item")
    for item in product_items:
        img_tag = item.find("img")
        if img_tag:
            images.append(os.getenv("KSIZE_URL") + img_tag["src"])
    
    return Product(name=name, short_description=short_description, images=images)