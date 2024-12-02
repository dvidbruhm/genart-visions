import datetime
from pathlib import Path


def get_file_name(dir_name: str, ext: str = ".png"):
    date_str = str(datetime.datetime.now()).replace(" ", "_").replace(".", "_").replace(":", "-")
    return Path(dir_name, date_str + ext)


def mkdir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)
