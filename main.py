import argparse
import logging
import time

from fuzzywuzzy import fuzz

from utils.image_preprocessing import ocr_image, save_still, still_to_pil
from utils.utils import load_config, make_filename
from utils.web_streaming import open_transmition

# %%
# logowanie zdarzeń
logger = logging.Logger(__file__)
formatter = logging.Formatter("%(asctime)s - %(message)s")
fh = logging.FileHandler("paski.log")
fh.setFormatter(formatter)
logger.addHandler(fh)


# %%
parser = argparse.ArgumentParser()
parser.add_argument(
    "-w",
    "--headless",
    dest="headless",
    action="store_true",
    help="Start browser with no head",
)
parser.add_argument(
    "-c",
    "--config",
    dest="config",
    type=str,
    default="config.yaml",
    help="Path to config file",
)

# %%
def main():
    args = parser.parse_args()
    config = load_config(args.config)

    driver = open_transmition(config["TVPStreamUrl"], args.headless)

    prev_ticker_text = ""
    while True:
        browser_image = driver.get_screenshot_as_png()
        frame_image = still_to_pil(
            browser_image,
            (
                config["frame"]["left"],
                config["frame"]["top"],
                config["frame"]["right"],
                config["frame"]["bottom"],
            ),
        )
        ticker_image = still_to_pil(
            browser_image,
            (
                config["ticker"]["left"],
                config["ticker"]["top"],
                config["ticker"]["right"],
                config["ticker"]["bottom"],
            ),
        )

        ticker_text = ocr_image(ticker_image)

        fz_ratio = fuzz.ratio(ticker_text, prev_ticker_text)
        fz_partial_ratio = fuzz.partial_ratio(ticker_text, prev_ticker_text)

        if (len(ticker_text) > 10) and ((fz_ratio < 70) or (fz_partial_ratio < 70)):
            prev_ticker_text = ticker_text

            logger.info(ticker_text)
            print(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')}: {fz_ratio=} | {fz_partial_ratio=}\n\t{ticker_text}"
            )

            # zapisanie zrzutu ekranu całej przeglądarki
            filename = make_filename(config["image_dir"], kind="frame")
            save_still(browser_image, filename, config)
            
            # zapisanie zrzutu ekranu tv
            filename = make_filename(config["image_dir"], kind="image")
            frame_image.save(filename)
            
            # zapisanie paska
            filename = make_filename(config["image_dir"], kind="pasek")
            ticker_image.save(filename)

        time.sleep(5)

        # reset browsera co godzinę - jakby się streaming przytkał na przykład
        if int(time.strftime("%M")) == 0:
            logger.info("[INFO] Zamykam przeglądarkę")
            driver.quit()
            logger.info("[INFO] Przeglądarka zamknięta")
            time.sleep(60)
            driver = open_transmition(config["TVPStreamUrl"], args.headless)


if __name__ == "__main__":
    main()
