import os
import time

import yaml


def make_filename(image_folder: str, kind: str) -> str:
    y, m, d, h = (
        time.strftime("%Y"),
        time.strftime("%m"),
        time.strftime("%d"),
        time.strftime("%H"),
    )
    fn = f"{image_folder}/{y}/{m}/{d}/{h}/{kind}/{time.strftime('%Y%m%d_%H%M%S')}.png"

    folder, _ = os.path.split(fn)
    try:
        os.makedirs(folder)
    except Exception as e:
        # print(e)
        pass

    return fn


def load_config(filename: str) -> dict:
    with open("config.yaml", "r") as f:
        c = yaml.safe_load(f)

    return c
