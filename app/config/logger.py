import logging


def setup_logger():
    logger = logging.getLogger("fastapi")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(log_format)

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
