import logging
import sys

from src.utils.config import config


def get_logger(name: str) -> logging.Logger:
    """
    Возвращает логгер для модуля.
    Использование: logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(config.log_level)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)-8s %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger
