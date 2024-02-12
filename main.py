import time

import yaml

import dir
import logger
from backup import Backup, del_old_backups, parse_date
from compress import compress


def delete_oldest(backups: list[str]) -> list[str]:
    backups.sort(key=lambda x: parse_date(dir.basename(x)))

    if len(backups) > 1:
        dir.delete(backups[0])
        backups.pop(0)

    return backups


if __name__ == '__main__':
    #
    #   Step 1: Load configuration
    #
    yamlfile: dict
    try:
        with open(f'{dir.srcfile()}/config.yml', 'r') as file:
            yamlfile = yaml.safe_load(file)
    except Exception as e:
        logger.fatal("Couldn't load config.yml!")
        logger.exception(e)
        exit(1)

    # Set console log level according to configuration
    logger.set_console_log_level(yamlfile['console_log_level'])

    #
    #   Step 2: Create a backup profile
    #
    try:
        backup: Backup = Backup(yamlfile['include'], yamlfile['destination'], yamlfile['keep'])
        logger.info(f'Keep: {backup.keep} backup(s)')
        logger.info(f'Backup: {backup.children}')
        logger.info(f'Destination: {backup.destination}')

        # Exit if there's nothing to compress
        total_size: int = len(backup)
        logger.info(f'{backup.filename} needs up to {total_size} bytes to store!')
        if total_size == 0:
            logger.error(f'There is nothing to backup!')
            exit(0)
    except Exception as e:
        logger.fatal('Error occurs while setting up backup file!')
        logger.exception(e)
        exit(3)

    try:
        #
        #   Step 3: Delete expired backups
        #
        del_old_backups(dir.scan_4_backup(backup.destination), yamlfile['delete_older_than'])

        #
        #   Step 4: Reduce the amount of backups to number defined in config.yml
        #
        if backup.keep > 0:
            backups: list[str] = dir.scan_4_backup(backup.destination)
            while len(backups) > backup.keep - 1:
                backups = delete_oldest(backups)
    except Exception as e:
        logger.fatal('Failed to make space for new backup!')
        logger.exception(e)

    #
    #   Step 5: Check for empty space
    #
    if total_size > dir.get_free_space(backup.destination):
        if yamlfile['remove_old_backups_for_space']:
            logger.error(f'Not enough space, deleting old backups in 5 seconds... [Ctrl + C] to cancel!')
            time.sleep(5)

            while total_size > dir.get_free_space(backup.destination) and len(backups) > 1:
                backups = delete_oldest(backups)

            if total_size > dir.get_free_space(backup.destination):
                logger.fatal(f'Failed to free up some space, exiting...')
                exit(2)
        else:
            logger.error(f'Not enough space, exiting...')
            exit(1)

    try:
        #
        #   Step 6: Compress all files
        #
        logger.info('Backing up. Please wait...')
        start: float = time.perf_counter()
        compress(backup)
        stop: float = time.perf_counter()
        logger.info(f'Backup finished in {stop - start} seconds')
    except Exception as e:
        logger.fatal('Error occurs while backing up!')
        logger.exception(e)
