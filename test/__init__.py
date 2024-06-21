from os.path import join
from platform import system

from src import PROJECT_DIR
from src import logger

logger.consoleHandler.setLevel(50)
logger.logger.removeHandler(logger.fileHandler)

valid_config: dict = {
    'console_log_level': 'DEBUG',
    'include': [],
    'destination': '',
    'compressed_file_name': 'zstd-backup',
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
    },
    'settings': {
        'write_chunk': 1024,
        'progress_bar': {
            'enabled': True
        }
    },
    'remote_storage': {
        'enabled': False,
        'type': 'SFTP',
        'server': {
            'host': '127.0.0.1',
            'port': 22
        },
        'credentials': {
            'protocol': 'ED25519',
            'username': 'username',
            'keypath': '',
            'passphrase': '',
            'remote_path': '/remote/location/compressed.zstd',
            'delete_after_transfer': False,
        }
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
