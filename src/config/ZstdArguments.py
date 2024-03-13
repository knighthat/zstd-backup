from multiprocessing import cpu_count

from src.logger import debug, warn
from src.utils.type import verify
from .Abstract import ConfigTemplate


class ZstdArguments(ConfigTemplate):

    def __init__(self, configuration: dict) -> None:
        super().__init__(configuration)

        #
        #   Compression level
        #
        self._level: int
        self._setLevel(self['level'])

        #
        #   Threads to use
        #
        self._threads: int
        self._setThreads(self['threads'])

    @property
    def level(self) -> int:
        """
        :return: an integer represents compression level
        """
        return self._level

    def _setLevel(self, value) -> None:
        """
        Set compression level

        :param value: level to compress
        """
        try:
            fromfile: int = verify(value, int)

            if fromfile > 22:
                # Warn about level exceeding limit
                warn(f'Maximum compression level is 22, got \'{fromfile}\'. Corrected to 22')
                # Correct to maximum number
                fromfile = 22

            self._level = fromfile

        except TypeError:
            warn(f'\'{value}\' is not a valid number! Corrected to 3.')
            self._level = 3

        debug(f'Compression level: {self.level}')

    @property
    def threads(self) -> int:
        """
        :return: an integer represents threads to use by program
        """
        return self._threads

    def _setThreads(self, value) -> None:
        """
        Set number of threads to do compression

        :param value: how many threads will be allocated to this program
        """
        try:

            fromfile: int = verify(value, int)

            if fromfile < 0:
                # Warn about sub-zero threads
                warn(f'Number of threads must be a positive number! Corrected to 0 (all threads).')
                fromfile = 0
            elif fromfile > cpu_count():
                # Warn about exceeding threads count
                warn(f'Number of threads cannot exceed number of available threads ({cpu_count()}! '
                     f'Corrected to 0 (all threads).')
                fromfile = 0

            self._threads = fromfile

        except TypeError:
            warn(f'\'{value}\' is not a valid number! Corrected to 0 (all threads).')
            self._threads = 0

        debug(f'Using {self.threads} to compress.')

    def __str__(self) -> str:
        return (
            'ZstdArgument('
            f'level={self.level}, '
            f'threads={self.threads}'
            ')'
        )
