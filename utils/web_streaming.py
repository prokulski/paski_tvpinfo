import time
from xmlrpc.client import boolean

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def open_transmition(tvpstream_url: str, headless: bool=True) -> webdriver:
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
    element = driver.find_element(By.XPATH, "//div[@class='tvp-covl__ab']")
    if element:
        element.click()

    # kliknięcie play
    element = driver.find_element(
        By.XPATH,
        "//div[@class='tp2thm tp2thm-icon tp2thm-icon-play tp2thm-icon-play-custom']",
    )
    element.click()
    time.sleep(1)

    return driver
