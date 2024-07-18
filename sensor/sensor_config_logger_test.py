from config import Config
from logger_br import logger

if __name__ == '__main__':
    config = Config()
    logger.debug(f"config:{Config.get('logger.level')}")
