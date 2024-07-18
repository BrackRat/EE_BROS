from loguru import logger
from datetime import datetime
import os
import sys


def setup_logger(level="DEBUG"):
    logs_directory = "logs"
    os.makedirs(logs_directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    log_filename = f"{logs_directory}/{timestamp}.log"
    logger.remove()  # Remove default handlers
    logger.add(log_filename, level=level, rotation="00:00", retention="1 day", compression="zip")
    logger.add(sys.stdout, level=level)


setup_logger()
