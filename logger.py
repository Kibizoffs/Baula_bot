import logging
from logging.handlers import RotatingFileHandler

from config import log

def _setup_logger():
    logger = logging.getLogger()
    level = logging.DEBUG # уровень отладки
    logger.setLevel(level)

    # отладка в файл
    file_handler = RotatingFileHandler(
        filename=log.file_path,
        maxBytes=log.max_size,
        backupCount=log.backup_count)
    file_handler.setLevel(level)
    file_handler.setFormatter(log.file_format)
    logger.addHandler(file_handler)

    # отладка в консоль
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log.stream_format)
    stream_handler.setLevel(level)
    logger.addHandler(stream_handler)

    return logger

logger = _setup_logger()
