import logging
import os

from src import __version__, __copyright__, PROJECT_DIR, today


# Set log's location and create folder if needed
workdir: str = os.path.join(PROJECT_DIR, 'logs')
os.makedirs(workdir, exist_ok=True)

# Log2File Handler
filename: str = f'{today.date()}.log'
filepath: str = os.path.join(workdir, filename)
fileHandler: logging = logging.FileHandler(filepath)
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


" Print copyright and license notice "
print(f'ZSTD Backup - {__version__}')
print(__copyright__, '\n')
