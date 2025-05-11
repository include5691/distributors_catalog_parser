import logging
from src.soup import get_soup
from src.schemas import Product
from src.common import CARSMART_URL





def get_product_links_car_smart(url: str, limit: int | None = None) -> list | None:
    """ """
    products = []
    page_num = 1
    while True:
        current_url = f"{url}?page={page_num}"
        soup = get_soup(current_url)
        if not soup:
            logging.error(f"Cant get soup for url {current_url}")
            break
        product_containers = soup.find_all("div", class_="catalog-list")
        if not product_containers:
            if page_num == 1 and not products:
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
                        if limit and len(products) >= limit:
                            return products
        page_num += 1
    return products
