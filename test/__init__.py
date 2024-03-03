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

TEST_DIR: str = join(PROJECT_DIR, 'test')

# Apply different path type depends on system
if system() == 'Windows':
    valid_config['include'] = [
        '.\\test\\include\\1',
        '.\\test\\include\\2',
        '.\\test\\include\\3',
        '.\\test\\include\\4',
        '.\\test\\include\\ignore'
    ]
    valid_config['destination'] = '.\\test\\backups'
    valid_config['ignore'] = '.\\test\\include\\ignore'
else:
    valid_config['include'] = [
        './test/include/1',
        './test/include/2',
        './test/include/3',
        './test/include/4',
        './test/include/ignore'
    ]
    valid_config['destination'] = './test/backups'
    valid_config['ignore'] = './test/include/ignore'
