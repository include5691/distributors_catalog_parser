import re
import logging
from urllib.parse import urljoin
from e5nlp import make_gpt_request
from au_b24 import notify_user

from src.soup import get_soup
from src.schemas import Product
from src.common import (
    CARSMART_URL,
    DISTRIBUTOR_NAME,
    OPENAI_MODEL_NAME,
    CARSMART_DESCRIPTION_PROMPT,
)


def _remove_brand_text(text: str) -> str:
    if not text:
        return
    return (
        text.replace("Car-Smart", DISTRIBUTOR_NAME)
        .replace("Car Smart", DISTRIBUTOR_NAME)
        .replace("CarSmart", DISTRIBUTOR_NAME)
    )


def get_product_links(url: str, limit: int | None = None) -> list | None:
    """Get product links from a Car Smart subcategory page"""
    links = []
    page_num = 1
    while True:
        current_url = f"{url}?page={page_num}"
        soup = get_soup(current_url)
        if not soup:
            logging.error(f"Cant get soup for url {current_url}")
            break
        product_containers = soup.find_all("div", class_="catalog-list")
        if not product_containers:
            if page_num == 1 and not links:
                logging.error(
                    f"No product containers found on the first page: {current_url}"
                )
                return None
            else:
                break
        for container in product_containers:
            product_cards = container.find_all("form", class_="product-preview")
            for card in product_cards:
                link_tag = card.find("a", class_="ekran-cover", href=True)
                if link_tag:
                    href = link_tag.get("href")
                    if href and href.startswith("/product/"):
                        full_url = CARSMART_URL + href
                        if full_url not in links:
                            links.append(full_url)
                        if limit and len(links) >= limit:
                            return links
        page_num += 1
    return links


def parse_product(url: str, categories_path: str | None = None) -> Product | None:
    soup = get_soup(url)
    if not soup:
        return None

    # name
    h1 = soup.find("h1", class_="product__title")
    name = h1.get_text(strip=True)

    # car name

    m = re.search(r"магнитола\s+для\s+(.*?)\s*-\s*", name, re.I) or re.search(
        r"магнитола\s+(.*?)\s*-\s*", name, re.I
    )
    if not m:
        logging.error(f"Car name not found in product name: {name} for url {url}")
        return None
    car_name = m.group(1).strip()
    name = f"Магнитола для {car_name}, {name[(name.find("Android") or -1):]}"

    # Short description
    meta = soup.find("meta", attrs={"name": "description"})
    short_description = _remove_brand_text(meta["content"])

    # Attributes
    attributes = {}
    prop_div = soup.find("div", id="product-characteristics")
    if prop_div:
        for item in prop_div.select(".property"):
            n = item.find(class_="property-name")
            v = item.find(class_="property-content")

            if n and v:
                n_text = n.get_text(strip=True)
                v_text = v.get_text(strip=True)
                if n_text == "Гарантия":
                    v_text = "2 года"
                if n_text == "Быстродействие":
                    continue
                attributes[n_text] = v_text

    # Description from table
    description_str = None
    chars = soup.find("div", class_="widget-type_auto-chars")
    if chars:
        table = chars.find("table")
        if table:
            desc_list = [
                f"{tds[0].get_text(strip=True)}: {tds[1].get_text(strip=True)}"
                for row in table.find_all("tr")
                if (tds := row.find_all("td")) and len(tds) == 2
            ]
            if desc_list:
                description_str = _remove_brand_text("\n".join(desc_list))
        ai_generated_description = make_gpt_request(
            text=name + description_str + str(attributes),
            prompt=CARSMART_DESCRIPTION_PROMPT,
            model_name=OPENAI_MODEL_NAME,
        )
        if not ai_generated_description:
            logging.error(f"AI generated description not found for url {url}")
            notify_user(16306, f"AI generated description not found for url {url}")
            exit()
        description = ai_generated_description

    # Images
    images = []
    imgs = soup.select(
        ".product__gallery .js-product-all-images .product__slide-main a.product__photo"
    ) or soup.select(".product__area-photo .product__photo[data-fslightbox]")
    for tag in imgs:
        href = tag.get("href")
        if href and not href.startswith(("javascript:", "data:image")):
            images.append(urljoin(CARSMART_URL, href) if href.startswith("/") else href)
    if not images:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            img_url = og["content"]
            images.append(
                urljoin(CARSMART_URL, img_url) if img_url.startswith("/") else img_url
            )

    try:
        return Product(
            name=name,
            categories_path=categories_path,
            car_name=car_name,
            short_description=short_description,
            description=_remove_brand_text(description),
            images=images,
            attributes=attributes,
        )
    except Exception:
        return None


def get_products(url: str, categories_path: str | None = None) -> list[Product] | None:
    "Get product by subcategory page"
    products = []
    links = get_product_links(url)
    if not links:
        logging.error(f"No product links found for URL: {url}")
        return None
    for link in links:
        product = parse_product(link, categories_path)
        if product:
            products.append(product)
        else:
            logging.error(f"Failed to parse product from link: {link}")
    return products
