from src.logger import warn


class OldBackupsSettings:
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

    def __init__(self, configuration: dict) -> None:
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

    def __str__(self) -> str:
        return (
            f'OldBackupSettings('
            f'keep={self.keep}, '
            f'retention={self.retention}, '
            f'del_old_4_space={self.del_old_4_space}, '
            f'aggressive={self.aggressive}'
            f')'
        )
