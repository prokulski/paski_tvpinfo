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

    last_pasek_ocr = ""
    while True:
        filename = make_filename(config["StillsFolder"])
        still = driver.get_screenshot_as_png()
        image = still_to_pil(
            still,
            (
                config["Ekran"]["left"],
                config["Ekran"]["top"],
                config["Ekran"]["right"],
                config["Ekran"]["bottom"],
            ),
        )
        pasek = still_to_pil(
            still,
            (
                config["Pasek"]["left"],
                config["Pasek"]["top"],
                config["Pasek"]["right"],
                config["Pasek"]["bottom"],
            ),
        )
        pasek_ocr = ocr_image(pasek)

        fz_ratio = fuzz.ratio(pasek_ocr, last_pasek_ocr)
        fz_partial_ratio = fuzz.partial_ratio(pasek_ocr, last_pasek_ocr)

        # print(f"{fz_ratio} | {fz_partial_ratio} | {pasek_ocr}  ", end="\r")

        if (len(pasek_ocr) > 10) and ((fz_ratio < 70) or (fz_partial_ratio < 70)):

            logger.info(pasek_ocr)
            print(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')}: {fz_ratio=} | {fz_partial_ratio=}\n\t{pasek_ocr}"
            )

            save_still(still, filename, config)  # zapisane całego zrzutu z ramkami
            # image.save(filename)  # zapisanie zrzutu ekranu
            last_pasek_ocr = pasek_ocr

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
