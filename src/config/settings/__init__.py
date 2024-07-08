from src.logger import debug, warn
from src.utils.type import verify
from .ProgressBar import ProgressBar
from ..Abstract import ConfigTemplate


class Settings(ConfigTemplate):

    def __init__(self, configuration: dict) -> None:
        super().__init__(configuration)

        #
        #   Write chunk
        #
        self._write_chunk: int
        self._setWriteChunk(self['write_chunk'])

        #
        #   Progress bar
        #
        self._progress_bar: ProgressBar
        self._setProgressBar(self['progress_bar'])

    @property
    def write_chunk(self) -> int:
        """
        :return: number of bytes program attempts to write each write cycle
        """
        return self._write_chunk

    def _setWriteChunk(self, value) -> None:
        """
        Set number bytes for each write cycle.
        Higher number can cause I/O bottleneck.
        Default value is 1024 bytes.

        :param value: an integer represents bytes
        """
        try:
            fromfile: int = verify(value, int)

            if fromfile <= 0:
                warn(f'\'settings.write_chunk\' must be a positive number! '
                     f'Corrected to 1024.')
                fromfile = 1024

            self._write_chunk = fromfile

        except TypeError:
            warn(f'Unrecognized input \'{value}\'. Use default value: 1024.')
            self._write_chunk = 1024

        debug(f'Write chunk: {self.write_chunk} bytes')

    @property
    def progress_bar(self) -> ProgressBar:
        """
        :return: an instance of ProgressBar class.
        """
        return self._progress_bar

    def _setProgressBar(self, value) -> None:
        """
        Convert a dictionary represents ProgressBar class.

        :param value: a dict contains necessary properties to parse ProgressBar
        """
        fromfile: dict = verify(value, dict)
        self._progress_bar = ProgressBar(fromfile)

        debug(f'Progress bar: {str(self.progress_bar)}')

    def __str__(self) -> str:
        return (
            'Settings('
            f'write_chunk={self.write_chunk},'
            f'progress_bar={str(self.progress_bar)}'
            ')'
        )
