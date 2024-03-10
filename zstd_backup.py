from os.path import join
from time import sleep, perf_counter

import yaml

from src import dir, logger, PROJECT_DIR
from src.backup import BackupProfile, del_old_backups
from src.compress import zstd_compress
from src.config import Configuration
from src.converter import size_converter, time_converter
from src.parser import parse_date


def delete_oldest(backups: list) -> list:
    backups.sort(key=lambda x: parse_date(dir.basename(x)))

    if len(backups) > 1:
        dir.delete(backups[0])
        backups.pop(0)

    return backups


if __name__ == '__main__':

    #
    #   Step 1: Load Configuration
    #
    configuration: Configuration
    try:
        with open(join(PROJECT_DIR, 'config.yml'), 'r') as file:
            configuration = Configuration(yaml.safe_load(file))

        # Load log level from config.yml
        logger.consoleHandler.setLevel(configuration.log_level)

        logger.debug(str(configuration))
    except Exception as e:
        logger.fatal("Couldn't load config.yml!")
        logger.exception(e)
        exit(1)

    #
    #   Step 2: Create a backup profile
    #
    profile: BackupProfile
    try:
        profile = BackupProfile(configuration)

        # Exit if there's nothing to compress
        total_size: int = len(profile)
        if total_size == 0:
            logger.error('There is nothing to backup!')
            exit(0)
        else:
            comp_size: str = size_converter(total_size)
            logger.info(f'{profile.filename} needs up to {comp_size} to store!')

        logger.debug(str(profile))
    except Exception as e:
        logger.fatal('Error occurs while setting up backup file!')
        logger.exception(e)
        exit(3)

    old_backups: list = dir.scan_4_backup(profile.destination)

    try:
        #
        #   Step 3: Delete expired backups
        #
        if configuration.old_backup_settings.retention > 0:

            del_old_backups(old_backups, configuration.old_backup_settings.retention)
            old_backups = dir.scan_4_backup(profile.destination)

        else:
            logger.info('Retention is set to 0 > Overdue backups will not be deleted!')

        #
        #   Step 4: Reduce the amount of backups to number defined in config.yml
        #
        if configuration.old_backup_settings.keep > 0:

            while len(old_backups) > configuration.old_backup_settings.keep - 1:
                old_backups = delete_oldest(old_backups)

        else:
            logger.info('Keep is set to 0 > Keep all old backups!')

    except Exception as e:
        logger.fatal('Failed to make space for new backup!')
        logger.exception(e)

    #
    #   Step 5: Check for empty space
    #
    if total_size > dir.get_free_space(profile.destination):
        if configuration.old_backup_settings.del_old_4_space:
            """
            If 'old_backups.remove_old_backups_for_space' is set to "true".
            Program will attempt to remove older backups in order to make
            space for new compressed file.
            """

            # Warn user about space inefficient, and give them 5 seconds to cancel the task
            logger.error('Not enough space, deleting old backups in 5 seconds... [Ctrl + C] to cancel!')
            sleep(5)

            while total_size > dir.get_free_space(profile.destination):
                if len(old_backups) == 0:
                    break

                if len(old_backups) > 1 and not configuration.old_backup_settings.aggressive:
                    """
                    Break while-loop if 'old_backups.aggressive' is set to "false"
                    and only 1 backup left. Otherwise, delete to the last one.
                    """
                    break

                old_backups = delete_oldest(old_backups)

        if total_size > dir.get_free_space(profile.destination):
            """
            If space is insufficient after old backups deletion
            or when old backup removal is not allowed, throw error
            then exit with code 2.
            """
            logger.fatal('Failed to free up some space, exiting...')
            exit(2)

    try:
        #
        #   Step 6: Start Compression
        #
        # Start timer
        start: float = perf_counter()

        # Begin compressing
        logger.info('Backing up. Please wait...')
        zstd_compress(profile, configuration)

        # Stop timer
        stop: float = perf_counter()
        logger.info(f'Backup finished in {time_converter(stop - start)}')
    except Exception as e:
        logger.fatal('Error occurs while backing up!')
        logger.exception(e)
