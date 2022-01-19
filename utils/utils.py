import os
import time

import yaml


def make_filename(stills_folder: str) -> str:
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    hour = time.strftime("%H")
    fn = f"{stills_folder}/{year}/{month}/{day}/{hour}/{time.strftime('%Y%m%d_%H%M%S')}.png"

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
