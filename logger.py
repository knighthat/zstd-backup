import logging
import os
from datetime import datetime

workdir = "./logs"
filename = f'{workdir}/{datetime.today().date()}.log'

os.makedirs('./logs', exist_ok=True)

# Log2File Handler
fileHandler: logging = logging.FileHandler(filename)
fileHandler.setLevel(logging.DEBUG)

# Log2Console Handler
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)


def set_console_log_level(level: str) -> None:
    lvl: int

    if level.lower() == 'debug':
        lvl = logging.DEBUG
    elif level.lower() == 'warn':
        lvl = logging.WARN
    elif level.lower() == 'error':
        lvl = logging.ERROR
    elif level.lower() == 'fatal':
        lvl = logging.FATAL
    else:
        lvl = logging.INFO
        
    consoleHandler.setLevel(lvl)


logging.basicConfig(
    format='[%(asctime)s / %(levelname)-8.8s] -> %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
    handlers=[fileHandler, consoleHandler]
)

logger = logging.getLogger()
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)


def debug(s: str):
    logger.debug(s)


def info(s: str):
    logger.info(s)


def warn(s: str):
    logger.warning(s)


def error(s: str):
    logger.error(s)


def fatal(s: str):
    logger.critical(s)


def exception(e: Exception):
    logger.exception(msg=e)


def eol():
    with open(filename, 'a') as log:
        log.write('/-----------------------/\n')
