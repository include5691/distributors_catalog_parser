import logging
from ._soup import get_soup
from ._common import KSIZE_URL

def get_subcategories_urls(url: str) -> list[str] | None:
    soup = get_soup(url)
    if soup is None:
        logging.error(f"Soup not found for url {url}")
        return None
    subcategories_menu = soup.find("div", class_="category-panel")
    if not subcategories_menu:
        logging.error(f"Subcategories menu not found for url {url}")
        return None
    subcategories_items = subcategories_menu.find_all("span")
    if not subcategories_items:
        logging.error(f"Subcategories not found for url {url}")
        return None
    subcategories = []
    for item in subcategories_items:
        a_tag = item.find("a")
        if a_tag:
            subcategories.append(KSIZE_URL + a_tag["href"])
    return subcategories