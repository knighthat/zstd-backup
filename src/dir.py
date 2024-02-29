import os
from enum import Enum
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



def prep(path: str) -> str:
    if folder_exist(path) != ReturnCode.EXIST:
        os.makedirs(path)

    path = abspath(path)
    logger.debug(f'Backup will be saved to: {path}')

    return path


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
    fs_stat: os = os.statvfs(of)
    free = fs_stat.f_frsize * fs_stat.f_bavail

    logger.debug(f'{free} bytes can be written into {of}')
    return free


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
    :param path: relative path to convert
    :return: same path but in absolute form
    """

    if os.path.isabs(path):
        """
        No further step needed if 'path'
        is already in absolute form.
        """
        return path

    if path.startswith('~/'):
        """
        Convert '~' into user's home directory
        """
        return os.path.expanduser(path)

    if path.startswith('./'):
        """
        os.path.abspath() replaces '.' with user's current directory.
        For example, './rel/path/file1' will be replaced by '$PWD/path/file1'
        """
        return path.replace('./', f'{PROJECT_DIR}/')

    """
    If no match found, append project's directory in front of it
    """
    return os.path.join(PROJECT_DIR, path)


def basename(path: str) -> str:
    return os.path.basename(path)
