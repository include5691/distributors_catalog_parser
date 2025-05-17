import re
import logging
from e5nlp import make_gpt_request
from au_b24 import notify_user
from src.soup import get_soup
from src.schemas import Product
from src.common import (
    KSIZE_URL,
    KSIZE_DESCRIPTION_PROMPT,
    DISTRIBUTOR_NAME,
    OPENAI_MODEL_NAME,
)


def get_product(url: str, categories_path: str | None = None) -> Product | None:
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
        short_description_li_tag = short_description_tag.find(
            "li", class_="s-nomenclature__main-attr"
        )
        if short_description_li_tag:
            short_description = " ".join(
                short_description_li_tag.get_text(strip=True)
                .replace("<br>", "\n")
                .split()
            ).replace("Wide Media", DISTRIBUTOR_NAME)
            short_description = short_description.replace('"', "")
    attributes = {}
    info_block = soup.find("div", class_="js-nomenclature_block")
    if info_block:
        items = info_block.find_all("tr")
        for tr in items:
            name_tag = tr.find("th")
            value_tag = tr.find("td")
            if name_tag and value_tag:
                value = value_tag.get_text(strip=True)
                attr_name = name_tag.get_text(strip=True)
                if attr_name == "Серия":
                    continue
                elif attr_name == "Производитель":
                    name = name.split(value)[0].strip()
                    if short_description:
                        short_description = short_description.replace(
                            value, DISTRIBUTOR_NAME
                        )
                    attr_value = DISTRIBUTOR_NAME
                else:
                    attr_value = value
                attributes[attr_name] = attr_value
    description = None
    description_tag = soup.find("div", itemprop="description")
    if description_tag:
        description = " ".join(
            description_tag.get_text(strip=True).replace("<br>", "\n").split()
        ).replace("Wide Media", DISTRIBUTOR_NAME)
        ai_generated_description = make_gpt_request(
            text=name + description + str(attributes),
            prompt=KSIZE_DESCRIPTION_PROMPT,
            model_name=OPENAI_MODEL_NAME,
        )
        if not ai_generated_description:
            logging.error(f"AI generated description not found for url {url}")
            notify_user(16306, f"AI generated description not found for url {url}")
            exit()
        description = ai_generated_description
        description = description.replace('"', "").replace(
            "Wide Media", DISTRIBUTOR_NAME
        )
    images = []
    product_items = soup.find_all("div", class_="s-nomenclature__photo-item")
    for item in product_items:
        img_tag = item.find("img")
        if img_tag:
            images.append(KSIZE_URL + img_tag["src"])
    car_name = None
    match_first_letter = re.search(r"[a-zA-Z]", name)
    if match_first_letter:
        car_name = name[match_first_letter.start() :].strip()
        name = "Магнитола для " + car_name
    return Product(
        name=name,
        categories_path=categories_path,
        car_name=car_name,
        short_description=short_description,
        description=description,
        images=images,
        attributes=attributes,
    )


def get_products(
    url: str, categories_path: str | None = None, limit: int | None = None
) -> list[Product] | None:
    "Get product by products page"
    products = []
    i = 1
    while True:
        soup = get_soup(url + f"?page={i}")
        if not soup:
            break
        products_group = soup.find(
            "div",
            class_="s-catalog-groups s-catalog-groups_layout_grid js-nomenclatures",
        )
        if not products_group:
            break
        products_items = products_group.find_all("a", class_="s-catalog-groups__link")
        if not products_items:
            break
        for item in products_items:
            product_url = KSIZE_URL + item["href"]
            product = get_product(product_url, categories_path)
            if product:
                products.append(product)
            if limit and len(products) >= limit:
                return products
        i += 1
    return products
