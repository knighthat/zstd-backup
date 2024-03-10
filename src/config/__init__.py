from __future__ import annotations

from logging import DEBUG, INFO, WARN, ERROR, FATAL

from src.logger import warn, debug
from src.utils.type import verify
from .OldBackupsSettings import OldBackupsSettings
from .ZstdArguments import ZstdArguments
from .settings import Settings


class Configuration:
    _configuration: dict

    def __init__(self, configuration: dict) -> None:
        self._configuration = configuration

        #
        #   Log level
        #
        self._log_level: int = INFO
        self._setLogLevel(self['console_log_level'])

        #
        #   Children
        #
        self._include: set = set()
        self._setChildren(self['include'])

        #
        #   Destination
        #
        self._destination: str
        self._setDestination(self['destination'])

        #
        #   Ignore paths
        #
        self._ignore_paths: set = set()
        self._setIgnorePaths(self['ignore'])

        #
        #   Old backups settings
        #
        self._old_backups_settings: OldBackupsSettings
        self._setOldBackupsSettings(self['old_backups'])

        #
        #   ZSTD arguments
        #
        self._zstd_arguments: ZstdArguments
        self._setZstdArguments(self['arguments'])

        #
        #   Settings
        #
        self._settings: Settings
        self._setSettings(self['settings'])

    @property
    def log_level(self) -> int:
        """
        Determine what console logs will be shown to users.
        Higher level means less outputs.

        Possible values: DEBUG, INFO, WARN, ERROR, FATAL

        :return: level as an integer
        """
        return self._log_level

    def _setLogLevel(self, value) -> None:
        """
        Parse 'value' to logging's level.
        If an unknown value is provided, use 'INFO' as fallback

        :param value: level in text

        :raise TypeError: if value's type wasn't str
        """
        # Confirms type of 'console_log_level'
        fromfile: str = verify(value, str, 'INFO')

        # Match value from 'console_log_level' to actual level (integer)
        if fromfile.upper() == 'DEBUG':
            self._log_level = DEBUG
        elif fromfile.upper() == 'WARN' or fromfile.upper() == 'WARNING':
            self._log_level = WARN
        elif fromfile.upper() == 'ERROR':
            self._log_level = ERROR
        elif fromfile.upper() == 'FATAL':
            self._log_level = FATAL
        elif fromfile.upper() != 'INFO':
            warn(f'Unknown log level: {fromfile}. Use "INFO" as fallback!')

        debug(f'Logging @ level \'{self.log_level}\'')

    @property
    def include(self) -> set:
        """
        :return: a set of paths to be included with the compressed file
        """
        return self._include

    def _setChildren(self, value) -> None:
        """
        Add path(s) from 'value'.

        :param value:
            can either be a string (single path) or list (multiple paths)

        :raise TypeError: if 'value' was neither a str nor a list
        """
        fromfile: str | list = verify(value, (list, str))

        if len(fromfile) == 0:
            # Path to be included in compressed file must not be empty
            raise Exception('Please provide at least 1 path to compress!')

        if isinstance(fromfile, str):
            # If provided value is a string, add it to set
            self._include.add(fromfile)
        else:
            # If provided value is a list, add all to set
            self._include.update(fromfile)

        debug(f'Include:  {", ".join(self.include)}')

    @property
    def destination(self) -> str:
        """
        :return: path to save compressed file
        """
        return self._destination

    def _setDestination(self, value) -> None:
        """
        Set location to save compressed file

        :param value: path to save file (relative path is OK)
        """
        fromfile: str = verify(value, str)

        if not fromfile:
            # Path to save compressed file must not be empty
            raise Exception('Empty destination!')
        else:
            self._destination = fromfile

        debug(f'Save compressed file to \'{self.destination}\'')

    @property
    def ignore_paths(self) -> set:
        """
        :return: paths that are not included with the compressed file
        """
        return self._ignore_paths

    def _setIgnorePaths(self, value) -> None:
        """
        Add path(s) to collection of path should NOT
        be included in the compressed file.

        :param value: a path or list of paths to be ignored
        """
        fromfile: str | list = verify(value, (list, str))

        if isinstance(fromfile, str):
            # If provided value is a string, add it to set
            self._ignore_paths.add(fromfile)
        else:
            # If provided value is a list, add all to set
            self._ignore_paths.update(fromfile)

        debug(f'Paths to ignore: {", ".join(self.ignore_paths)}')

    @property
    def old_backups_settings(self) -> OldBackupsSettings:
        """
        :return: an instance of OldBackupsSettings
        """
        return self._old_backups_settings

    def _setOldBackupsSettings(self, value) -> None:
        """
        Create an instance of OldBackupsSettings from
        provided dictionary.

        :param value: dict contains keys of 'old_backups' from config.yml
        """
        fromfile: dict = verify(value, dict)
        self._old_backups_settings = OldBackupsSettings(fromfile)

        debug(f'Old backups settings: {str(self.old_backups_settings)}')

    @property
    def zstd_arguments(self) -> ZstdArguments:
        """
        :return: an instance of ZstdArguments
        """
        return self._zstd_arguments

    def _setZstdArguments(self, value) -> None:
        """
        Create an instance of ZstdArguments from
        provided dictionary.

        :param value: dict contains keys of 'arguments' from config.yml
        """
        fromfile: dict = verify(value, dict)
        self._zstd_arguments = ZstdArguments(fromfile)

        debug(f'ZSTD arguments: {str(self.zstd_arguments)}')

    @property
    def settings(self) -> Settings:
        """
        :return: an instance of Settings
        """
        return self._settings

    def _setSettings(self, value) -> None:
        """
        Create an instance of Settings from
        provided dictionary.

        :param value: dict contains keys of 'settings' from config.yml
        """
        fromfile: dict = verify(value, dict)
        self._settings = Settings(fromfile)

        debug(f'Settings: {str(self.settings)}')

    def __exist__(self, item: str) -> bool:
        return item in self._configuration

    def __getitem__(self, item: str):
        if not self.__exist__(item):
            raise KeyError(f'\'{item}\' does NOT exist!')
        return self._configuration[item]

    def __str__(self) -> str:
        return (
            'Configuration('
            f'level={self.log_level}, '
            f'include={str(self.include)}, '
            f'destination={self.destination}, '
            f'ignore={str(self.ignore_paths)}, '
            f'OldBackupSettings={str(self.old_backups_settings)}, '
            f'ZstdArguments={str(self.zstd_arguments)}'
            ')'
        )
