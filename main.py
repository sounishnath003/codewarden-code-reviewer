from codewarden.config import Configuration


def main():
    conf = Configuration()
    conf.logger.debug("running the codewarden in DEBUG log mode")

    for i in range(10):
        conf.logger.info("logging the index={%d}; square={%d}", i, i * i)

    conf.logger.debug("execution completed")


if __name__ == "__main__":
    main()
