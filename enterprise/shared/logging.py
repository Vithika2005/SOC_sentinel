# enterprise/shared/logging.py

import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a file handler which logs even debug messages
    fh = RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 5, backupCount=5)
    fh.setLevel(logging.DEBUG)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger
