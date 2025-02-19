import logging
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

def get_soup(url: str) -> BeautifulSoup | None:
    "Get BeautifulSoup object from url"
    try:
        with requests.Session() as session:
            response = session.get(url)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
    except RequestException as e:
        logging.error(f"Request error: {e} for url {url}")
