import logging
import requests
from requests.exceptions import RequestException

def get_html(url: str) -> str | None:
    try:
        with requests.Session() as session:
            response = session.get(url)
            if response.status_code == 200:
                return response.text
    except RequestException as e:
        logging.error(f"Request error: {e} for url {url}")
