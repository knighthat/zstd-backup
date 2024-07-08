from src.logger import debug, warn
from src.utils.type import verify
from ..Abstract import ConfigTemplate


class ProgressBar(ConfigTemplate):

    def __init__(self, configuration: dict) -> None:
        super().__init__(configuration)

        #
        #   On/Off
        #
        self._enabled: bool
        self._setEnabled(self['enabled'])

    @property
    def enabled(self) -> bool:
        """
        :return: whether program bar is enabled
        """
        return self._enabled

    def _setEnabled(self, value) -> None:
        try:
            self._enabled = verify(value, bool)
        except TypeError:
            warn(f'Unrecognized input \'{value}\'. Use default value: False.')
            self._enabled = False

        debug(f'Enable progress bar? {self.enabled}')

    def __str__(self) -> str:
        return f'ProgressBar(enabled={self.enabled})'
