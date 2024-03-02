import ctypes
import os
from enum import Enum
from pathlib import Path
from platform import system
from re import match
from shutil import rmtree

from src import PROJECT_DIR, logger


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


def scan_4_backup(destination: str) -> list[str]:
    """
    Scan provided path, parse any file that matches
    compressed file's format. Add it to a list and return
    :param destination: directory to scan
    :return: a list of files matched format
    """
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
    """
    Calculate and return the number of bytes
    can be written to this path.
    :param of: path to calculate free space
    :return: available space in bytes
    """
    result: int

    if system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(of),
            None,
            None,
            ctypes.pointer(free_bytes)
        )
        result = free_bytes.value
    else:
        fs_stat: os = os.statvfs(of)
        result = fs_stat.f_frsize * fs_stat.f_bavail

    logger.debug(f'{result} bytes can be written into {of}')
    return result


def delete(path: str) -> None:
    """
    Delete physical file/folder
    :param path: to delete
    """
    if os.path.isdir(path):
        rmtree(path)
        logger.info(f'Deleted directory:  {path}')
    elif os.path.isfile(path):
        os.remove(path)
        logger.info(f'Deleted file: {path}')
    else:
        logger.info(f'Failed to delete {path}: Unknown type!')


def abspath(path: str) -> str:
    """
    Convert relative path to absolute path
    This function uses pathlib.Path to convert
    to system's path before returning.
    :param path: relative path to convert
    :return: same path but in absolute form
    """
    result: str

    if os.path.isabs(path):
        """
        No further step needed if 'path'
        is already in absolute form.
        """
        result = path
    elif path.startswith('~/'):
        " Convert '~' into user's home directory "
        result = os.path.expanduser(path)
    elif path.startswith('./'):
        """
        os.path.abspath() replaces '.' with user's current directory.
        For example, './rel/path/file1' will be replaced by '$PWD/path/file1'
        """
        result = path.replace('./', f'{PROJECT_DIR}/')
    else:
        " If no match found, append project's directory in front of it "
        result = os.path.join(PROJECT_DIR, path)

    return Path(result).__str__()


def basename(path: str) -> str:
    return os.path.basename(path)
