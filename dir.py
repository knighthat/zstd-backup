import os
from enum import Enum
from inspect import getsourcefile
from re import match

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
    match folder_exist(path):
        case ReturnCode.EXIST:
            pass
        case _:
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
    os.remove(path)
    logger.info(f'Deleted {path}!')


def abspath(path: str) -> str:
    if path.startswith('~'):
        logger.debug(f'Convert {path} to {os.path.expanduser(path)}')
        path = os.path.expanduser(path)

    abspath = os.path.abspath(path)
    logger.debug(f'Absolute path of {path} is {abspath}')

    return abspath


def basename(path: str) -> str:
    return os.path.basename(path)


def srcfile() -> str:
    return os.path.dirname(getsourcefile(lambda: 0))
