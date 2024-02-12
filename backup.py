import os
from datetime import datetime, timedelta

import dir
import logger

today = datetime.today()
time_format = "%Y-%b-%d %H-%M-%f"


class Backup:

    def __init__(self, backup: list[str], destination: str, keep: int) -> None:
        self._set_destination(destination)
        self._set_children(backup)
        self._set_keep(keep)
        self.filename = f'{today.strftime(time_format)}.zstd'

    def _set_destination(self, path: str) -> None:
        if not path:
            path = os.path.join(dir.srcfile(), 'backups')
            logger.warn(f'Empty or null destination! Using {path}')

        self.destination = dir.prep(path)

    def _set_children(self, paths: list[str]) -> None:
        self.children: list[str] = []

        for p in paths:
            path = dir.abspath(p)
            if not os.path.exists(path):
                logger.warn(f'{path} does not exist! Skipping...')
            else:
                self.children.append(path)

    def _set_keep(self, history: int) -> None:
        result: int = 0
        try:
            if int(history) < 0:
                logger.error(f'{history} is not a positive number!')
                logger.error(f'Using default value: 0')
            else:
                result = history
        except TypeError as e:
            logger.exception(e)
            logger.error(f'{history} is not a valid number!')
            logger.error(f'Using default value: 0')

        self.keep = result

    def __len__(self) -> int:

        def _size(abspath: str, total: int) -> int:
            try:
                return total + os.path.getsize(abspath)
            except FileNotFoundError:
                logger.warn(f'Error while reading {abspath}! Could be broken link (shortcut). Skipping...')
            except Exception as e:
                logger.warn(f'Error while calculating size of {abspath}')
                logger.exception(e)

        def _dir_size(abspath: str, total: int) -> int:
            for root, dirs, names in os.walk(abspath):
                for name in names:
                    filepath = os.path.join(root, name)
                    return _size(filepath, total)

        size: int = 0
        for file in self.children:
            if os.path.isfile(file):
                size += _size(file, size)
            elif os.path.isdir(file):
                size += _dir_size(file, size)

        return size


def parse_date(filename: str) -> datetime:
    return datetime.strptime(filename.split('.')[0], time_format)


def del_old_backups(backups: list[str], days: int) -> None:
    logger.info(f'Deleting old backups that were created {days} day(s) ago...')
    if len(backups) == 0:
        logger.info('No old backup found! Skipping this step...')

    try:
        for file in backups:
            basename: str = dir.basename(file)
            if today - parse_date(basename) > timedelta(days=days):
                dir.delete(file)
    except Exception as e:
        logger.error(f'Error occurs while deleting old backups!')
        logger.exception(e)
