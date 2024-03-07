from src.logger import warn


class ZstdArguments:
    # Higher values are slower but yield smaller size.
    # More at: https://python-zstandard.readthedocs.io/en/latest/compressor.html#zstdcompressor
    level: int = 3
    # How many threads should the program use.
    # More threads equals faster compression time.
    # 0 will use all threads (also the default)
    threads: int = 0

    def __init__(self, configuration: dict) -> None:
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

    def __str__(self) -> str:
        return (
            f'ZstdArgument('
            f'level={self.level}, '
            f'threads={self.threads}'
            f')'
        )
