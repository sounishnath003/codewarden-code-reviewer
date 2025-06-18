import logging

logging.basicConfig(
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
    style="%",
    format="[%(levelname)s]:%(name)s:%(asctime)s: %(message)s",
)

LOGGER = logging.getLogger("Codearden")
