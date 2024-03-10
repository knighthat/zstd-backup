from src.logger import debug, warn
from src.utils.type import verify


class ProgressBar:
    _configuration: dict

    def __init__(self, configuration: dict) -> None:
        self._configuration = configuration

        #
        #   On/Off
        #
        self._enabled: bool
        self._setEnabled(self['enabled'])

    @property
    def enabled(self) -> bool:
        return self._enabled

    def _setEnabled(self, value) -> None:
        try:
            self._enabled = verify(value, bool, force_cast=True)
        except TypeError:
            warn(f'Unrecognized input \'{value}\'. Use default value: False.')
            self._enabled = False

        debug(f'Enable progress bar? {self.enabled}')

    def __exist__(self, item: str) -> bool:
        return item in self._configuration

    def __getitem__(self, item: str):
        if not self.__exist__(item):
            raise KeyError(f'\'{item}\' does NOT exist!')
        return self._configuration[item]

    def __str__(self) -> str:
        return f'ProgressBar(enabled={self.enabled})'
