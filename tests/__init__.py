from os import makedirs
from os.path import join

from src import PROJECT_DIR

valid_config: dict = {
    'console_log_level': 'DEBUG',
    'include': [
        './tests/include/1',
        './tests/include/2',
        './tests/include/3',
        './tests/include/4',
        './tests/include/ignore'
    ],
    'destination': './tests/backups',
    'ignore': './tests/include/ignore',
    'old_backups': {
        'keep': 1,
        'retention': 2,
        'remove_old_backups_for_space': False,
        'aggressive': True
    },
    'arguments': {
        'level': 1,
        'threads': 2
    }
}

TEST_DIR: str = join(PROJECT_DIR, 'tests')


def make_test_files() -> None:
    """
    Create 'include' directory inside tests/
    with each subdirectory contains text files
    from 1 to 5
    """
    for subdir in ['1', '2', '3', '4', 'ignore']:
        makedirs(f'{TEST_DIR}/include/{subdir}', exist_ok=True)
        for name in [1, 2, 3, 4, 5]:
            # /path/to/project/tests/include/ignore/1.txt
            filepath: str = f'{TEST_DIR}/include/{subdir}/{name}.txt'

            " Each text file has about 5KiB of null data "
            with open(filepath, 'wb') as file:
                file.seek(1024 - 1)
                file.write(b"\0")
