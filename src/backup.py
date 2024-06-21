import os
from datetime import timedelta, datetime
from functools import cache
import re

from src import today, time_format, PROJECT_DIR, dir, logger
from src.config import Configuration
from src.parser import parse_date


match_all_pattern = re.compile(r'^:[^:]+:$')
match_partial_pattern = re.compile(r'^;[^;]+;$')


class BackupProfile:
    def __init__(self, config: Configuration):
        #
        #   Ignore paths
        #
        self.ignore = set()
        for path in config.ignore_paths:
            abspath: str
            if match_all_pattern.match(path) or match_partial_pattern.match(path):
                abspath = path
            else:
                abspath = dir.abspath(path)
            self.ignore.add(abspath)

        #
        #   Destination path
        #
        self.destination = dir.abspath(config.destination)
        if dir.folder_exist(self.destination) != dir.ReturnCode.EXIST:
            os.makedirs(self.destination)
        logger.debug(f'Backup will be saved to: {self.destination}')

        #
        #   Paths to compress
        #
        self._set_children(config.include)

        #
        #   Name of compressed file
        #
        self.filename = f'{config.filename}.zstd'

    @property
    def size(self):
        return self.__len__()

    def _set_children(self, paths: set) -> None:
        """
        Loop through provided paths, and add filtered
        paths to 'self.children'
        :param paths: to compress
        """
        self.children = set()

        def _add_file(path: str) -> None:
            """
            Add 'path' to 'self.children' if
            path isn't listed in 'self.ignore_paths'
            :param path: to compress
            """
            ignore_file: bool = False
            
            for ign in self.ignore:
                if match_all_pattern.match(ign):
                    ignore_file = re.compile(ign[1:-1]).match(path)
                elif match_partial_pattern.match(ign):
                    ignore_file = re.compile(ign[1:-1]).search(path)
                else:
                    ignore_file = path.startswith(ign)
                
                if ignore_file:
                    break

            if ignore_file:
                logger.debug(f'Ignore {path}!')
            else:
                self.children.add(path)

        def _add_dir(path: str) -> None:
            """
            Loop through every single file inside this folder
            and use '_add_file()' to add file's path to 'self.children'
            :param path: to loop through
            """
            for root, dirs, files in os.walk(path):
                for name in files:
                    _add_file(os.path.join(root, name))

        for p in paths:
            " Convert path to absolute path "
            abspath = dir.abspath(p)
            if not os.path.exists(abspath):
                " If path doesn't exist, skip next step "
                logger.warn(f'{abspath} does not exist! Skipping...')
                continue

            " Path can be either folder or file, use appropriate function for each"
            if os.path.isdir(abspath):
                _add_dir(abspath)
            elif os.path.isfile(abspath):
                _add_file(abspath)

    @cache
    def __len__(self) -> int:
        """
        Calculate the size (in bytes)
        of the total files add up.
        :return: total size of children in bytes
        """

        def _size(abspath: str) -> int:
            """
            :param abspath: path to file or folder
            :return: size in bytes
            """
            try:
                return os.path.getsize(abspath)
            except FileNotFoundError:
                logger.warn(f'Error while reading {abspath}! Could be a broken link (shortcut). Skipping...')
            except Exception as e:
                logger.warn(f'Error while calculating size of {abspath}! Skipping...')
                logger.exception(e)

            return 0

        def _dir_size(abspath: str) -> int:
            """
            Calculate directory's size by adding each file
            inside the folder (including files inside sub-folder).
            :param abspath: path to folder
            :return: size in bytes
            """
            total: int = 0
            for root, dirs, names in os.walk(abspath):
                for name in names:
                    filepath = os.path.join(root, name)
                    total += _size(filepath)

            return total

        size: int = 0
        for file in self.children:
            if os.path.isfile(file):
                size += _size(file)
            elif os.path.isdir(file):
                size += _dir_size(file)

        return size

    def __str__(self) -> str:
        return f'BackupProfile(name={self.filename}, size={len(self)})'


class Backup:

    def __init__(self, backup: list, destination: str, keep: int, ignore: list = None) -> None:
        self.ignore = [] if ignore is None else ignore
        self._set_destination(destination)
        self._set_children(backup)
        self._set_keep(keep)
        self.filename = f'{today.strftime(time_format)}.zstd'

    def _set_destination(self, path: str) -> None:
        if not path:
            path = os.path.join(PROJECT_DIR, 'backups')
            logger.warn(f'Empty or null destination! Using {path}')

        self.destination = dir.abspath(path)
        if dir.folder_exist(self.destination) != dir.ReturnCode.EXIST:
            os.makedirs(self.destination)
        logger.debug(f'Backup will be saved to: {self.destination}')

    def _set_children(self, paths: list) -> None:
        self.children = []

        def _add_file(path: str) -> None:
            for ign in self.ignore:
                if path.startswith(ign):
                    logger.debug(f'Ignore {path}!')
                else:
                    self.children.append(path)

        def _add_dir(path: str) -> None:
            for root, dirs, files in os.walk(path):
                for name in files:
                    _add_file(os.path.join(root, name))

        for p in paths:
            abspath = dir.abspath(p)
            if not os.path.exists(abspath):
                logger.warn(f'{abspath} does not exist! Skipping...')
                continue

            if os.path.isdir(abspath):
                _add_dir(abspath)
            elif os.path.isfile(abspath):
                _add_file(abspath)

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

        def _size(abspath: str) -> int:
            try:
                return os.path.getsize(abspath)
            except FileNotFoundError:
                logger.warn(f'Error while reading {abspath}! Could be broken link (shortcut). Skipping...')
            except Exception as e:
                logger.warn(f'Error while calculating size of {abspath}')
                logger.exception(e)

            return 0

        def _dir_size(abspath: str) -> int:
            total: int = 0
            for root, dirs, names in os.walk(abspath):
                for name in names:
                    filepath = os.path.join(root, name)
                    total += _size(filepath)

            return total

        size: int = 0
        for file in self.children:
            if os.path.isfile(file):
                size += _size(file)
            elif os.path.isdir(file):
                size += _dir_size(file)

        return size


def del_old_backups(old_backup_paths: list, days: int) -> None:
    logger.info(f'Deleting old backups that were created {days} day(s) ago...')
    if len(old_backup_paths) == 0:
        logger.info('No old backup found! Skipping this step...')

    delta: timedelta = timedelta(days=days)
    old_backups: list = [OldBackup(x) for x in old_backup_paths]
    
    try:
        for backup in old_backups:
            if today - backup.ctime > delta:
                dir.delete(backup.filepath)
    except Exception as e:
        logger.error(f'Error occurs while deleting old backups!')
        logger.exception(e)   


class OldBackup:
    def __init__(self, filepath: str) -> None:
        # Check if file exists or is file
        if not os.path.exists(filepath):
            logger.warn(f'{filepath} does not exist!')
            return
        elif not os.path.isfile(filepath):
            logger.warn(f'{filepath} is not a file!')
            return
        
        self._filepath = filepath
        self._ctime = os.path.getctime(filepath)
        
    @property
    def filepath(self) -> str:
        return self._filepath
    
    @property
    @cache
    def ctime(self) -> datetime:
        return datetime.fromtimestamp(self._ctime)
        