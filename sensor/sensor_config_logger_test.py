from config import Config
from logger_br import logger

if __name__ == '__main__':
    config = Config()
    print(Config.get('logger.level'))
    logger.debug(f"config:{Config.get('logger.level')}")
