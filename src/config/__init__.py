from logging import DEBUG, INFO, WARN, ERROR, FATAL
from multiprocessing import cpu_count as cpus
from os.path import join

from src import PROJECT_DIR
from src.logger import warn
from .OldBackupsSettings import OldBackupSettings
from .ZstdArguments import ZstdArguments
from .settings import Settings


class Configuration:
    log_level: int = INFO
    include = set()
    destination: str = join(PROJECT_DIR, 'backups')
    ignore_paths = set()
    old_backup_settings: OldBackupSettings
    zstd_arguments: ZstdArguments
    settings: Settings

    def __init__(self, configuration: dict) -> None:
        #
        #   Set Logging Level
        #
        log_level = configuration['console_log_level']
        # If value of 'console_log_level' is not a string,
        # then set 'log_level' to its str value
        if not isinstance(log_level, str):
            log_level = str(log_level)

        # Determine log level or throw warning and use default value (INFO)
        if log_level.upper() == 'DEBUG':
            self.log_level = DEBUG
        elif log_level.upper() == 'WARN' or log_level.upper() == 'WARNING':
            self.log_level = WARN
        elif log_level.upper() == 'ERROR':
            self.log_level = ERROR
        elif log_level.upper() == 'FATAL':
            self.log_level = FATAL
        elif log_level.upper() != 'INFO':
            warn(f'Unknown log level: {log_level}. Use "INFO" as fallback!')

        #
        #   Add Include Paths
        #
        include = configuration['include']
        if not isinstance(include, list):
            # If 'include' isn't a list of paths but a
            # single string, then add that string as
            # 1 of the children. Otherwise, throw error
            # and return code 1
            if isinstance(include, str):
                self.include.add(str(include))
            else:
                raise TypeError('Value of "include" is not a string')
        else:
            # Add all provided paths to set
            for path in include:
                self.include.add(path)

        #
        #   Set Destination
        #
        destination = configuration['destination']
        if not isinstance(destination, str):
            # Raise error and exit if 'destination'
            # isn't a string.
            raise TypeError('Destination must be a string!')
        self.destination = str(destination)

        #
        #   Set Ignore Paths
        #
        ignore = configuration['ignore']
        if not isinstance(ignore, list):
            # If 'ignore' isn't a list of paths but a
            # single string, then add that string as
            # 1 of the children. Otherwise, raise error
            if isinstance(ignore, str):
                self.ignore_paths.add(str(ignore))
            else:
                raise TypeError('Value of "ignore" is not a string')
        else:
            # Add all provided paths to set
            for path in ignore:
                self.ignore_paths.add(path)

        #
        #   Set Old Backup Settings
        #
        self.old_backup_settings = OldBackupSettings(configuration['old_backups'])

        #
        #   Set ZSTD Arguments
        #
        self.zstd_arguments = ZstdArguments(configuration['arguments'])

        #
        #   Set Settings
        #
        self.settings = Settings(configuration['settings'])

    def __str__(self) -> str:
        return (
            f'Configuration('
            f'level={self.log_level}, '
            f'include={str(self.include)}, '
            f'destination={self.destination}, '
            f'ignore={str(self.ignore_paths)}, '
            f'OldBackupSettings={str(self.old_backup_settings)}, '
            f'ZstdArguments={str(self.zstd_arguments)}'
            f')'
        )


def verify(config: Configuration) -> bool:
    """
    Verify and apply correction (if applicable).

    :param config: configuration instance to check
    :return: only returns False if error is uncorrectable
    """

    if config.old_backup_settings.keep < 0:
        warn(f'"old_backups.keep" cannot be a sub-zero number! Corrected to 0.')
        config.old_backup_settings.keep = 0

    if config.old_backup_settings.retention < 0:
        warn(f'"old_backups.retention" cannot be a sub-zero number! Corrected to 0.')
        config.old_backup_settings.retention = 0

    if config.zstd_arguments.level > 22:
        warn(f'"arguments.level" must not exceeds 22')
        config.zstd_arguments.level = 22

    if config.zstd_arguments.threads < 0:
        warn(f'"arguments.threads" cannot be a sub-zero number! Corrected to 0.')
        config.zstd_arguments.threads = 0

    if config.zstd_arguments.threads == 0:
        config.zstd_arguments.threads = cpus()

    return True
