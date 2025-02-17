import logging
from bs4 import BeautifulSoup
from ._html import get_html
from ._common import KSIZE_URL

def get_subcategories(url: str) -> list[str] | None:
    html_content = get_html(url)
    if html_content is None:
        return None
    menu_soup = BeautifulSoup(html_content, "html.parser")
    subcategories_menu = menu_soup.find("div", class_="category-panel")
    subcategories_soup = BeautifulSoup(str(subcategories_menu), "html.parser")
    subcategories_items = subcategories_soup.find_all("span")
    if not subcategories_items:
        logging.error(f"Subcategories not found for url {url}")
        return None
    subcategories = []
    for item in subcategories_items:
        a_tag = item.find("a")
        if a_tag:
            subcategories.append(KSIZE_URL + a_tag["href"])
    return subcategories