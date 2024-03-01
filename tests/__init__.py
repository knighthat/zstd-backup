from os.path import join
from platform import system

from src import PROJECT_DIR

valid_config: dict = {
    'console_log_level': 'DEBUG',
    'include': [],
    'destination': '',
    'ignore': '',
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

# Apply different path type depends on system
if system() == 'Windows':
    valid_config['include'] = [
        '.\\tests\\include\\1',
        '.\\tests\\include\\2',
        '.\\tests\\include\\3',
        '.\\tests\\include\\4',
        '.\\tests\\include\\ignore'
    ]
    valid_config['destination'] = '.\\tests\\backups'
    valid_config['ignore'] = '.\\tests\\include\\ignore'
else:
    valid_config['include'] = [
        './tests/include/1',
        './tests/include/2',
        './tests/include/3',
        './tests/include/4',
        './tests/include/ignore'
    ]
    valid_config['destination'] = './tests/backups'
    valid_config['ignore'] = './tests/include/ignore'
