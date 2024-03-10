from src.logger import debug, info, warn
from src.utils.type import verify


class OldBackupsSettings:
    _configuration: dict

    def __init__(self, configuration: dict) -> None:
        self._configuration = configuration

        #
        #   Old backups to keep
        #
        self._keep: int
        self._setKeep(self['keep'])

        #
        #   Retention
        #
        self._retention: int
        self._setRetention(self['retention'])

        #
        #   Remove old backups for space
        #
        self._del_old_4_space: bool
        self._setDelOld4Space(self['remove_old_backups_for_space'])

        #
        #   Aggressive removal
        #
        self._aggressive: bool
        self._setAggressive(self['aggressive'])

    @property
    def keep(self) -> int:
        return self._keep

    def _setKeep(self, value) -> None:
        """
        Set number of old backups to keep

        :param value: number of old backups to keep
        """
        try:
            fromfile: int = verify(value, int)

            if fromfile < 0:
                # Warn about negative number
                warn(f'Number of old backup to keep must be greater or equal to 0! '
                     f'Corrected to 0 (no deletion).')
                # Correct to 0
                fromfile = 0

            self._keep = fromfile

        except TypeError:
            warn(f'Unrecognized input \'{value}\'. Use default value: 0.')
            self._keep = 0

        debug(f'Number of old backups to keep: {self.keep}')
        if self.keep == 0:
            info(f'Number of backups to keep is set to 0. '
                 f'Keep all unless it is overdue for deletion')

    @property
    def retention(self) -> int:
        return self._retention

    def _setRetention(self, value) -> None:
        """
        Set days to keep old backups

        :param value: number of days before an old backup gets expire
        """
        try:
            fromfile: int = verify(value, int)

            if fromfile < 0:
                # Warn about negative number
                warn(f'Number of retention days must be greater or equal to 0! '
                     f'Corrected to 0 (no deletion).')
                # Correct to 0
                fromfile = 0

            self._retention = fromfile

        except TypeError:
            warn(f'Unrecognized input \'{value}\'. Use default value: 0.')
            self._retention = 0

        debug(f'Delete backups older than: {self.keep} day(s)')
        if self.retention == 0:
            info(f'Retention is set to 0. Keep all backups regardless of creation date.')

    @property
    def del_old_4_space(self) -> bool:
        """
        :return: whether the program will delete recent backups for space
        """
        return self._del_old_4_space

    def _setDelOld4Space(self, value) -> None:
        """
        Set whether program delete older backups (after retention and keep)
        for space to fit new backup.

        :param value: True, False, 0, or 1
        """
        try:
            self._del_old_4_space = verify(value, bool, force_cast=True)
        except TypeError:
            warn(f'Unrecognized input \'{value}\'. Use default value: False.')
            self._del_old_4_space = False

        debug(f'Delete older backups for space: {self.del_old_4_space}')

    @property
    def aggressive(self) -> bool:
        """
        Only works if 'remove_old_backups_for_space' is enabled

        If True, the program will delete most recent backup
        in order to make space for new compressed file.
        Otherwise, it'll keep the most recent backup.

        :return: whether the program will delete most recent backup for space
        """
        return self._aggressive

    def _setAggressive(self, value) -> None:
        """
        Set whether program delete most recent backup
        (after retention, keep, old backups deletion)
        to make space for new backup.

        :param value: True, False, 0, or 1
        """
        try:
            self._aggressive = verify(value, bool, force_cast=True)
        except TypeError:
            warn(f'Unrecognized input \'{value}\'. Use default value: False.')
            self._aggressive = False

        debug(f'Delete older backups for space: {self.aggressive}')

    def __exist__(self, item: str) -> bool:
        return item in self._configuration

    def __getitem__(self, item: str):
        if not self.__exist__(item):
            raise KeyError(f'\'{item}\' does NOT exist!')
        return self._configuration[item]

    def __str__(self) -> str:
        return (
            'OldBackupSettings('
            f'keep={self.keep}, '
            f'retention={self.retention}, '
            f'del_old_4_space={self.del_old_4_space}, '
            f'aggressive={self.aggressive}'
            ')'
        )
