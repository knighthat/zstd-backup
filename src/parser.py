from datetime import datetime

from src import time_format


def parse_date(filename: str) -> datetime:
    return datetime.strptime(filename.split('.')[0], time_format)
