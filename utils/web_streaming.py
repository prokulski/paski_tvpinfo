import time
from xmlrpc.client import boolean

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def click_element(driver, xpath):
    """Kliknięcie w element - najpierw na niego czekamy, potem klikamy"""
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    button.click()


def open_transmition(tvpstream_url: str, headless: bool = True) -> webdriver:
    # wersja headless
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # bez okna
        chrome_options.add_argument("--mute-audio")  # bez audio

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(tvpstream_url)
    time.sleep(2)

    # skalowanie okna przeglądarki do konkretnej wielkości + zmiana croppingu
    driver.set_window_size(1280, 900)

    # zamknięcie okna z popupem
    click_element(driver, "//div[@class='tvp-covl__ab']")

    # kliknięcie play
    click_element(
        driver,
        "//div[@class='tp2thm tp2thm-icon tp2thm-icon-play tp2thm-icon-play-custom']",
    )

    time.sleep(1)

    return driver
