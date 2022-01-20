from io import BytesIO

import pytesseract
from PIL import Image, ImageDraw, ImageEnhance, ImageOps


def still_to_pil(selenium_png, cropping):
    im = Image.open(BytesIO(selenium_png))
    cropped_image = im.crop(cropping)
    return cropped_image


def preprocess_img(im, settings):
    # TODO: przerobić na openCV i zrobić sensowny preprocessing
    # tu https://github.com/yardstick17/image_text_reader/tree/master/image_preprocessing są dobre tricki

    # Contrast
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(settings["contrast"])

    # Sharpness
    enhancer = ImageEnhance.Sharpness(im)
    im = enhancer.enhance(settings["sharpness"])

    im = ImageOps.grayscale(im)

    if settings["show"]:
        im.show()
    return im


def ocr_image(image):
    settings = {"contrast": 1.25, "sharpness": 1.25, "show": False}

    # preprocess
    im_to_ocr = preprocess_img(image, settings)

    # OCR
    tesseract_options = """--psm 7"""
    ocr_text = pytesseract.image_to_string(
        im_to_ocr, lang="pol", config=tesseract_options
    )

    # text cleaning
    ocr_text = ocr_text.strip()

    # TODO: weryfikacja czy przeczytany tekst jest sensowny czy też znaki są losowe

    # usunięcie linii zaczynającej się zwykle od 'PILNE:'
    ocr_text = [txt for txt in ocr_text.split("\n") if "PILNE" not in txt.strip()]

    return " ".join(ocr_text)


def save_still(still, filename, config):
    # create  rectangleimage
    im = Image.open(BytesIO(still))
    rect = ImageDraw.Draw(im)
    rect.rectangle(
        [
            (config["Pasek"]["left"], config["Pasek"]["top"]),
            (config["Pasek"]["right"], config["Pasek"]["bottom"]),
        ],
        fill=None,
        outline="yellow",
        width=3,
    )
    rect.rectangle(
        [
            (config["Ekran"]["left"], config["Ekran"]["top"]),
            (config["Ekran"]["right"], config["Ekran"]["bottom"]),
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
