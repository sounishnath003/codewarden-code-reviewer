import logging
from typing import Literal

LogLevel = Literal["INFO", "DEBUG", "ERROR"]

LoggerFormat = {
    "level": logging.INFO,
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "style": "%",
    "format": "[%(levelname)s]:%(name)s:%(asctime)s:%(filename)s:%(lineno)d: %(message)s",
}


def init_logger():
    logging.basicConfig(**LoggerFormat)
    return logging.getLogger("Codewarden")
