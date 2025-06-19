import argparse

import yaml
from codewarden.config import Configuration


def init_config() -> Configuration | None:
    """parses the runtime --config file and return the Configuration instance for the project as defined"""
    parser = argparse.ArgumentParser("codewarden")
    # add the arguments
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="provide the config yaml file for your environment",
    )

    opts, pipeline_opts = parser.parse_known_args()
    conf = None

    with open(opts.config, "r+", encoding="utf-8") as file:
        print("trying to read config file", opts.config)
        config = yaml.safe_load(file)
        print("config", config)
        conf = Configuration(**config)
        file.close()

    return conf


def main():
    conf = init_config()
    if not conf:
        raise Exception("no configuration provided")


if __name__ == "__main__":
    main()
