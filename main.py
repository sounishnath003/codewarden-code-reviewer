import yaml
import argparse
import logging

from codewarden.command import logger
from codewarden.core.config import Configuration


def init_config() -> Configuration | None:
    """parses the runtime --config file and return the Configuration instance for the project as defined"""
    # create a argument parser
    parser = argparse.ArgumentParser("codewarden")
    # add the arguments
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="provide the config yaml file for your environment",
    )
    # parse the pipeline args and unknown args
    opts, pipeline_opts = parser.parse_known_args()
    conf = None
    # try to open config and read the yaml and parse it
    with open(opts.config, "r+", encoding="utf-8") as file:
        logging.info("trying to read config file %s", opts.config)
        config = yaml.safe_load(file)
        logging.info("config %s", config)
        conf = Configuration(**config)
        file.close()

    return conf


def main():
    # initialize the configuration for the project
    conf = init_config()
    if not conf:
        raise Exception("no configuration provided")

    conf.logger.info("i am a INFO log message")
    conf.logger.debug("i am a DEBUG log message")
    conf.logger.warning("i am a WARNING log message")


if __name__ == "__main__":
    logging.basicConfig(**logger.LoggerFormat)
    main()
