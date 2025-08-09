import logging
from pathlib import Path


def get_logger(name):
    """Возвращает настроенный логгер для приложения"""
    logger = logging.getLogger(f'{Path(__file__).parent.name}.{name}')
    return logger
