"""Dtek shutdown scraper app."""

import time
import os
import json
import argparse
from dataclasses import dataclass
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

_STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(_STATIC_DIR, exist_ok=True)

_WEBDRIVER_OPTIONS = Options()
_WEBDRIVER_OPTIONS.add_argument("--headless")
_WEBDRIVER_OPTIONS.add_argument("--window-size=1920,1080")
_WEBDRIVER = webdriver.Firefox(options=_WEBDRIVER_OPTIONS)

_ELEM_APPEARANCE_TIMEOUT = 5

_WEBDRIVER.get("https://www.dtek-dnem.com.ua/ua/shutdowns")


@dataclass
class Config:
    """Config."""

    user: str
    city: str
    street: str
    house: str

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create Config from dict."""
        return cls(
            user=data["user"],
            city=data["city"],
            street=data["street"],
            house=data["house"],
        )

    @classmethod
    def from_path(cls, path: str) -> "Config":
        """Create Config from file path."""
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        data["user"] = os.path.basename(path).split(".")[0]

        return cls.from_dict(data)


_PARSER = argparse.ArgumentParser()
_PARSER.add_argument(
    "-c", "--config", help="Path to config file", default="configs/home.json"
)
_CONFIG = Config.from_path(_PARSER.parse_args().config)


def _close_notification_popup():
    try:
        button = WebDriverWait(_WEBDRIVER, _ELEM_APPEARANCE_TIMEOUT).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "modal__close.m-attention__close")
            )
        )
    except TimeoutException:
        return

    button.click()


def main():
    """Run the app."""
    _close_notification_popup()

    city = WebDriverWait(_WEBDRIVER, _ELEM_APPEARANCE_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "city"))
    )
    city.send_keys(_CONFIG.city)

    cities_list = WebDriverWait(_WEBDRIVER, _ELEM_APPEARANCE_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "cityautocomplete-list"))
    )
    city_item = cities_list.find_element(By.TAG_NAME, "div").find_element(
        By.TAG_NAME, "strong"
    )
    city_item.click()

    street = _WEBDRIVER.find_element(By.ID, "street")
    street.send_keys(_CONFIG.street)
    streets_list = WebDriverWait(_WEBDRIVER, _ELEM_APPEARANCE_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "streetautocomplete-list"))
    )
    street_item = streets_list.find_element(By.TAG_NAME, "div").find_element(
        By.TAG_NAME, "strong"
    )
    street_item.click()

    # wait house to be clickable
    WebDriverWait(_WEBDRIVER, _ELEM_APPEARANCE_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "house_num"))
    )

    house = _WEBDRIVER.find_element(By.ID, "house_num")
    house.send_keys(_CONFIG.house)
    houses_list = WebDriverWait(_WEBDRIVER, _ELEM_APPEARANCE_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "house_numautocomplete-list"))
    )
    house_item = houses_list.find_element(By.TAG_NAME, "div").find_element(
        By.TAG_NAME, "strong"
    )
    house_item.click()

    _WEBDRIVER.execute_script("window.scrollBy(0, 350);")
    time.sleep(0.5)
    _WEBDRIVER.save_screenshot(os.path.join(_STATIC_DIR, f"{_CONFIG.user}_today.png"))

    els = _WEBDRIVER.find_elements(By.CLASS_NAME, "date")
    els[-1].click()
    _WEBDRIVER.save_screenshot(
        os.path.join(_STATIC_DIR, f"{_CONFIG.user}_tomorrow.png")
    )


if __name__ == "__main__":
    try:
        main()
    finally:
        _WEBDRIVER.quit()
