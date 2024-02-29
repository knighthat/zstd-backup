import os
import shutil
import unittest
from datetime import datetime, timedelta
from inspect import getsourcefile

import backup
from dir import scan_4_backup
from src.parser import parse_date


def curdir() -> str:
    relpath: str = os.path.dirname(getsourcefile(lambda: 0))
    return os.path.abspath(relpath)


class DateParsingTests(unittest.TestCase):
    valid_dates = [
        "2024-Feb-24 00-01-000001",
        "2024-Feb-25 00-02-000002",
        "2024-Feb-26 00-03-000003",
        "2024-Feb-27 00-04-000004",
        "2024-Feb-28 00-05-000005",
        "2024-Feb-29 00-06-000006",
        "2024-Mar-01 00-07-000007",
        "2024-Mar-02 00-08-000008",
        "2024-Mar-03 00-09-000009",
        "2024-Mar-04 00-10-000010",
    ]
    invalid_dates = [
        "24-Feb-2024 08-15-000000",
        "File1",
        "06-Apr-2024 19-25-000000",
        "Unk-2-2024 10-30-000000",
        "19-Jun-2024 05-35-000000",
        "11-Jul-2024 20-40-000000",
        "2024-Mar-03 26-09-000009",
        "25-Sep-2024 11-50-000000",
        "17-Oct-2024 06-55-000000",
        "Nov-08-2024 22-00-000000",
    ]

    def test_valid_parse_date(self) -> None:
        for date in self.valid_dates:
            try:
                parse_date(date)
            except:
                self.fail(f'{date} is invalid!')

    def test_invalid_parse_date(self) -> None:
        for date in self.invalid_dates:
            try:
                parse_date(date)
                self.fail(f'{date} is valid!')
            except:
                continue


class DeleteOlBackupTests(unittest.TestCase):
    today = datetime.now()

    @classmethod
    def setUp(cls):
        def _get_date_ago(days: int) -> str:
            """
            Get the date `days` days ago from today.

            Args:
                days (int): Number of days ago.

            Returns:
                str: Date in the format "%Y-%b-%d %H-%M-%f".
            """
            target_date = backup.today - timedelta(days)
            return target_date.strftime(backup.time_format)

        # Create 'backups' folder, ignore if exists
        os.makedirs('backups', exist_ok=True)

        # Create empty .zstd files with names
        # are dates ranging from 1 to 40
        days = [1, 2, 5, 10, 20, 30, 31, 35, 40]
        for day in days:
            filename = f'backups/{_get_date_ago(day)}.zstd'
            with open(filename, 'w'):
                pass

    @classmethod
    def tearDown(cls):
        shutil.rmtree('backups')

    def test_del_old_backups(self):
        values = {
            40: 8,
            35: 7,
            31: 6,
            30: 5,
            20: 4,
            10: 3,
            5: 2,
            2: 1,
            1: 0
        }
        backups: list[str] = scan_4_backup('backups')

        for days, remain in values.items():
            backup.del_old_backups(backups, days)

            backups = scan_4_backup('backups')
            self.assertEqual(
                len(backups),
                remain,
                f'The remaining backups after deleting backups that are older than {days} days must be {remain}'
            )


class BackupClassTest(unittest.TestCase):
    incl: str = os.path.join(curdir(), 'includes')
    include: list[str]
    dest: str = os.path.join(curdir(), 'backups')
    keep: int = 1
    ignore: list[str] = [os.path.join(incl, 'ignore')]
    instance: backup.Backup

    @classmethod
    def setUp(cls):

        def _create(parent: str) -> None:
            for i in range(10):
                with open(f'{parent}/file{i}.txt', 'w'):
                    pass

        os.makedirs(cls.incl, exist_ok=True)
        _create(cls.incl)

        subdir: list[str] = ['1', '2', '3', '4', 'ignore']
        for folder in subdir:
            path = os.path.join(cls.incl, folder)
            os.makedirs(path, exist_ok=True)
            _create(path)

        cls.include: list[str] = []
        for root, dirs, names in os.walk(cls.incl):
            for name in names:
                filepath = os.path.join(root, name)
                cls.include.append(filepath)

        cls.instance = backup.Backup(cls.include, cls.dest, 1, cls.ignore)

    @classmethod
    def tearDown(cls):
        shutil.rmtree(cls.incl)
        shutil.rmtree(cls.dest)

    def test_destination(self):
        self.assertTrue(os.path.exists('backups'))

    def test_children(self):
        for child in self.instance.children:
            for ign in self.ignore:
                self.assertFalse(
                    child.startswith(ign),
                    f'{ign} is marked for ignore but {child} is included!'
                )


if __name__ == '__main__':
    unittest.main()
