import os
from enum import Enum
from inspect import getsourcefile
from re import match
from shutil import rmtree

import logger


class ReturnCode(Enum):
    NOT_EXIST = 0
    EXIST = 1
    WRONG_TYPE = 2


def folder_exist(path: str) -> ReturnCode:
    result: ReturnCode
    if not os.path.exists(path):
        result = ReturnCode.NOT_EXIST
    elif os.path.isfile(path):
        result = ReturnCode.WRONG_TYPE
    else:
        result = ReturnCode.EXIST

    logger.debug(f'folder_exist({path}) returns {str(result)}')
    return result


def file_exist(path: str) -> ReturnCode:
    result: ReturnCode
    if not os.path.exists(path):
        result = ReturnCode.NOT_EXIST
    elif os.path.isdir(path):
        result = ReturnCode.WRONG_TYPE
    else:
        result = ReturnCode.EXIST

    logger.debug(f'file_exist({path}) returns {str(result)}')
    return result


def prep(path: str) -> str:
    path = abspath(path)
    logger.debug(f'Backup will be saved to: {path}')

    if folder_exist(path) != ReturnCode.EXIST:
        os.makedirs(path)

    return path


def scan_4_backup(destination: str) -> list[str]:
    results: list[str] = []
    if not folder_exist(destination):
        logger.warn(f'{destination} is not a directory!')
        return results

    filepattern: str = r'\d{4}-\w{3}-\d{2} \d{2}-\d{2}-\d{6}.zstd'
    for file in os.listdir(destination):
        if match(filepattern, file):
            results.append(os.path.join(destination, file))

    logger.debug(f'Found ({len(results)}) backup(s): {results}')
    return results


def get_free_space(of: str) -> int:
    fs_stat: os = os.statvfs(of)
    free = fs_stat.f_frsize * fs_stat.f_bavail

    logger.debug(f'{free} bytes can be written into {of}')
    return free


def delete(path: str) -> None:
    if os.path.isdir(path):
        rmtree(path)
        logger.info(f'Deleted directory:  {path}')
    elif os.path.isfile(path):
        os.remove(path)
        logger.info(f'Deleted file: {path}')
    else:
        logger.info(f'Failed to delete {path}: Unknown type!')


def abspath(path: str) -> str:
    absolute: str = ''
    if os.path.isabs(path):
        absolute = path
    if path.startswith('~'):
        logger.debug(f'Convert {path} to {os.path.expanduser(path)}')
        absolute = os.path.expanduser(path)
    elif path.startswith('.'):
        appd = path[2:] if path[1] == '/' else path
        absolute = os.path.join(srcfile(), appd)

    if not absolute:
        raise ValueError(f'Unknown path: {path}')

    if path != absolute:
        logger.debug(f'Absolute path of {path} is {absolute}')

    return absolute


def basename(path: str) -> str:
    return os.path.basename(path)


def srcfile() -> str:
    return os.path.dirname(getsourcefile(lambda: 0))
