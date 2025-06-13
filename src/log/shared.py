import logging
from .formatters import ColoredFormatter

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter())
logger.addHandler(handler)
logger.propagate = False

def get_logger():
    return logger
