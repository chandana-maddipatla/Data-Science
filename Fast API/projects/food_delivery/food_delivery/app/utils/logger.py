import logging
import sys


def setup_logger(name: str = "food_delivery") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    ))
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


logger = setup_logger()
