logger = logging.getLogger()

fileHandler = logging.handlers.RotatingFileHandler(
    filename="debug.log", maxBytes=10*1024*1024, backupCount=1)
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
