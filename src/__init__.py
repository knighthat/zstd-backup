from datetime import datetime
from os.path import abspath, dirname

__version__: str = '0.0.2'
__license__: str = 'MIT License'
__author__: str = 'knighthat'
__url__: str = 'https://github.com/knighthat/zstd-backup'
__copyright__: str = 'Copyright (C) 2023-2024, Knight Hat <https://github.com/knighthat>'

PROJECT_DIR: str = abspath(dirname(dirname(__file__)))
today: datetime = datetime.today()
time_format: str = "%Y-%b-%d %H-%M-%f"
