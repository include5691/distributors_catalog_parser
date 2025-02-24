import logging
from .model import Product
from .._soup import get_soup
from .._common import KSIZE_URL

def get_product(url: str) -> Product | None:
    "Get product by direct link"
    soup = get_soup(url)
    if not soup:
        return None
    title_tag = soup.find("h1")
    if not title_tag:
        logging.error(f"Title not found for url {url}")
    name = title_tag.get_text(strip=True)
    short_description = None
    short_description_tag = soup.find("div", class_="s-nomenclature__main-attr-first")
    if short_description_tag:
        short_description_li_tag = short_description_tag.find("li", class_="s-nomenclature__main-attr")
        if short_description_li_tag:
            short_description = short_description_li_tag.get_text(strip=True)
    description = None
    description_tag = soup.find("div", itemprop="description")
    if description_tag:
        description = short_description_tag.get_text(strip=True)
    images = []
    product_items = soup.find_all("div", class_="s-nomenclature__photo-item")
    for item in product_items:
        img_tag = item.find("img")
        if img_tag:
            images.append(KSIZE_URL + img_tag["src"])
    attributes = {}
    info_block = soup.find("div", class_="js-nomenclature_block")
    if info_block:
        items = info_block.find_all("tr")
        for tr in items:
            name_tag = tr.find("th")
            value_tag = tr.find("td")
            if name_tag and value_tag:
                attr_name = name_tag.get_text(strip=True)
                if attr_name == "Серия":
                    continue
                elif attr_name == "Производитель":
                    attr_value = "Element-5"
                else:
                    attr_value = value_tag.get_text(strip=True)
                attributes[attr_name] = attr_value
    return Product(name=name, short_description=short_description, description=description, images=images, attributes=attributes)

def get_products(url: str, limit: int | None = None) -> list[Product] | None:
    "Get product by products page"
    products = []
    i = 1
    while True:
        soup = get_soup(url + f"?page={i}")
        if not soup:
            break
        products_group = soup.find("div", class_="s-catalog-groups s-catalog-groups_layout_grid js-nomenclatures")
        if not products_group:
            break
        products_items = products_group.find_all("a", class_="s-catalog-groups__link")
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