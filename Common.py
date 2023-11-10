from datetime import datetime
import configparser
import pathlib
from pathlib import Path

def get_timestamp():
    return int(datetime.timestamp(datetime.now()) * 1000)

def get_config(section, option):
    config = configparser.ConfigParser()
    path_config = Path(pathlib.Path.cwd(), "Config.ini")
    config.read(path_config)

    return config.get(section, option)