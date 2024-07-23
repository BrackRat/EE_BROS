from loguru import logger
from datetime import datetime
import os
import sys
from config import Config


def setup_logger():
    level = Config.get("logger.level") or "INFO"
    logs_directory = "logs"
    os.makedirs(logs_directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    log_filename = f"{logs_directory}/{timestamp}.log"
    logger.remove()  # Remove default handlers
    logger.add(log_filename, level=level, rotation="00:00", retention="1 day", compression="zip")
    console_format = ("<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{"
                      "function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    logger.add(sys.stdout, level=level, format=console_format)

    logger.info(r"""
       ___  ___  ____  ____
      / _ )/ _ \/ __ \/ __/
     / _  / , _/ /_/ /\ \  
    /____/_/|_|\____/___/   [Ver 0.0.1]
    """)


setup_logger()
