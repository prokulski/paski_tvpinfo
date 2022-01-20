from io import BytesIO

import pytesseract
from PIL import Image, ImageDraw, ImageEnhance, ImageOps


def still_to_pil(selenium_png, cropping):
    im = Image.open(BytesIO(selenium_png))
    cropped_image = im.crop(cropping)
    return cropped_image


def preprocess_img(im: Image, settings: dict) -> Image:
    # TODO: przerobić na openCV i zrobić sensowny preprocessing
    # tu https://github.com/yardstick17/image_text_reader/tree/master/image_preprocessing są dobre tricki

    im = ImageOps.grayscale(im)

    # Contrast
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(settings["contrast"])

    # Sharpness
    enhancer = ImageEnhance.Sharpness(im)
    im = enhancer.enhance(settings["sharpness"])

    if settings["show"]:
        im.show()
    return im


def ocr_image(image: Image) -> str:
    settings = {"contrast": 1.5, "sharpness": 2, "show": False}

    # preprocess
    im_to_ocr = preprocess_img(image, settings)

    # OCR
    tesseract_options = """--psm 6"""
    ocr_text = pytesseract.image_to_string(im_to_ocr, lang="pol")

    # text cleaning
    ocr_text = ocr_text.strip()

    # TODO: weryfikacja czy przeczytany tekst jest sensowny czy też znaki są losowe

    # usunięcie linii zaczynającej się zwykle od 'PILNE:'
    # ocr_text = [txt.strip() for txt in ocr_text.split("\n") if "PILNE" not in txt.strip()]
    ocr_text = [txt.strip() for txt in ocr_text.split("\n")]

    return " ".join(ocr_text)


def save_still(still: bytes, filename: str, config: dict) -> None:
    # create  rectangleimage
    im = Image.open(BytesIO(still))
    rect = ImageDraw.Draw(im)
    rect.rectangle(
        [
            (config["ticker"]["left"], config["ticker"]["top"]),
            (config["ticker"]["right"], config["ticker"]["bottom"]),
        ],
        fill=None,
        outline="yellow",
        width=3,
    )
    rect.rectangle(
        [
            (config["frame"]["left"], config["frame"]["top"]),
            (config["frame"]["right"], config["frame"]["bottom"]),
        ],
        fill=None,
        outline="yellow",
        width=3,
    )

    # resize
    width, height = im.size
    newsize = (int(width / 2), int(height / 2))
    im = im.resize(newsize)
    im.save(filename)
