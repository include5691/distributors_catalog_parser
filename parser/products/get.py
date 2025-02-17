import logging
from bs4 import BeautifulSoup
from .model import Product
from .._html import get_html
from .._common import KSIZE_URL

def get_product(url: str) -> Product | None:
    "Get product by direct link"
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

def get_products(url: str, limit: int | None = None) -> list[Product] | None:
    "Get product by products page"
    products = []
    i = 1
    while True:
        html_content = get_html(url + f"?page={i}")
        if html_content is None:
            break
        group_soup = BeautifulSoup(html_content, "html.parser")
        products_group = group_soup.find("div", class_="s-catalog-groups s-catalog-groups_layout_grid js-nomenclatures")
        if not products_group:
            break
        products_soup = BeautifulSoup(str(products_group), "html.parser")
        products_items = products_soup.find_all("a", class_="s-catalog-groups__link")
        if not products_items:
            break
        for item in products_items:
            product_url = KSIZE_URL + item["href"]
            product = get_product(product_url)
            if product:
                products.append(product)
            if limit and len(products) >= limit:
                return products
        i += 1
    return products if products else None