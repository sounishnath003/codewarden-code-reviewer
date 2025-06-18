import logging
from attr import dataclass

from codewarden.logger import LOGGER


@dataclass
class Configuration:
    logger: logging.Logger = LOGGER
