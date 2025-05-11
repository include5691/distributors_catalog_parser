import logging
from src.soup import get_soup
from src.common import CARSMART_URL


def get_subcategories_urls(url: str) -> list[str] | None:
    soup = get_soup(url)
    selectors_container = soup.find("div", class_="selector-auto-selects")
    if not selectors_container:
        logging.error("No 'selector-auto-selects' container.")
        return None
    brand_select_div = selectors_container.find("div", class_="selector-auto-first")
    if not brand_select_div:
        logging.error("No selector 'selector-auto-first'")
        return None
    brand_select_tag = brand_select_div.find("select", class_="js-select-item")
    if not brand_select_tag:
        logging.error("Tag <select> with 'js-select-item' class not found.")
        return None

    subcategories = []
    for brand_option in brand_select_tag.find_all("option"):
        brand_value_slug = brand_option.get("value")
        subcategories.append(f"{CARSMART_URL}/collection/{brand_value_slug}")
    return subcategories
