import logging
from logging.handlers import RotatingFileHandler

from config import log

def _setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO) # общий уровень отладки

    fileHandler = RotatingFileHandler(
        filename=log.file_path, maxBytes=log.max_size, backupCount=log.backup_count)
    fileHandler.setLevel(logging.INFO) # уровень отладки файла
    fileHandler.setFormatter(log.file_format)
    logger.addHandler(fileHandler)

    streamHandler = logging.StreamHandler() # уровень отладки в консоли
    streamHandler.setLevel(logging.INFO)
    streamHandler.setFormatter(log.stream_format)
    logger.addHandler(streamHandler)

    return logger

logger = _setup_logger()
