from logging import DEBUG, INFO, WARN, ERROR, FATAL
from multiprocessing import cpu_count as cpus
from os.path import join

from src import PROJECT_DIR
from src.logger import warn


class OldBackupSettings:
    # Number of backups to keep
    # Only keep when it's not
    # overdue for deletion.
    keep: int = 5
    # If a backup's creation date
    # exceeds this number, it'll
    # be deleted.
    retention: int = 30
    # Should this program delete
    # older backups (even if it was
    # within retention days and
    # total files less than 'keep')
    # to save space for new backup.
    # This option always keeps the most
    # recent backup unless 'aggressive'
    # is set to True.
    del_old_4_space: bool = False
    # If True, delete to the last backup
    # to make some space for new backup
    aggressive: bool = False

    def __init__(self, configuration: dict):
        #
        #   Set Keep
        #
        keep = configuration['keep']
        if isinstance(keep, int):
            self.keep = int(keep)
        else:
            warn(f'{keep} is not a valid number for "old_backups.keep!"')
            warn(f'Use default value: {self.keep}')

        #
        #   Set Retention
        #
        retention = configuration['retention']
        if isinstance(retention, int):
            self.retention = int(retention)
        else:
            warn(f'{retention} is not a valid number for "old_backups.retention!"')
            warn(f'Use default value: {self.retention}')

        #
        #   Set Delete Old Backups For Space Boolean
        #
        del_old_4_space = configuration['remove_old_backups_for_space']
        if isinstance(del_old_4_space, bool):
            self.del_old_4_space = del_old_4_space
        else:
            warn('"old_backups.remove_old_backups_for_space must be a True or False!')
            warn(f'Use default value: {self.del_old_4_space}')

        #
        #   Set Aggressive Boolean
        #
        aggressive = configuration['aggressive']
        if isinstance(aggressive, bool):
            self.aggressive = aggressive
        else:
            warn('"old_backups.aggressive must be a True or False!')
            warn(f'Use default value: {self.aggressive}')

    def __str__(self):
        return (f'OldBackupSettings('
                f'keep={self.keep}, '
                f'retention={self.retention}, '
                f'del_old_4_space={self.del_old_4_space}, '
                f'aggressive={self.aggressive}'
                f')')


class ZstdArguments:
    # Higher values are slower but yield smaller size.
    # More at: https://python-zstandard.readthedocs.io/en/latest/compressor.html#zstdcompressor
    level: int = 3
    # How many threads should the program use.
    # More threads equals faster compression time.
    # 0 will use all threads (also the default)
    threads: int = 0

    def __init__(self, configuration: dict):
        #
        #   Set Compression Level
        #
        level = configuration['level']
        if isinstance(level, int):
            self.level = level
        else:
            warn(f'{level} is not a valid number for "arguments.level!"')
            warn(f'Use default value: {self.level}')

        #
        #   Set Number of Threads
        #
        threads = configuration['threads']
        if isinstance(threads, int):
            self.threads = threads
        else:
            warn(f'{threads} is not a valid number for "arguments.threads!"')
            warn(f'Use default value: {self.threads}')

    def __str__(self):
        return (f'ZstdArgument('
                f'level={self.level}, '
                f'threads={self.threads}'
                f')')


class Configuration:
    log_level: int = INFO
    include: set[str] = set()
    destination: str = join(PROJECT_DIR, 'backups')
    ignore_paths: set[str] = set()
    old_backup_settings: OldBackupSettings
    zstd_arguments: ZstdArguments

    def __init__(self, configuration: dict):
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

    def __str__(self):
        return (f'Configuration('
                f'level={self.log_level}, '
                f'include={str(self.include)}, '
                f'destination={self.destination}, '
                f'ignore={str(self.ignore_paths)}, '
                f'OldBackupSettings={str(self.old_backup_settings)}, '
                f'ZstdArguments={str(self.zstd_arguments)}'
                f')')


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
