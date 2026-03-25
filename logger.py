import logging
import os

LOG_FILE = "bot.log"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # File handler – saves everything
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.DEBUG)

    # Console handler – only INFO and above
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
