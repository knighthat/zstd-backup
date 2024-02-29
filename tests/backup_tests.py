import os
import shutil
import unittest
from datetime import datetime, timedelta
from re import match

from src import backup, config, time_format
from src.dir import scan_4_backup
from tests import valid_config, TEST_DIR


class BackupProfileTest(unittest.TestCase):
    incl_dir: str = os.path.join(TEST_DIR, 'include')
    profile: backup.BackupProfile

    @classmethod
    def setUpClass(cls):
        # Make 'include' folder in tests, skip if exists
        os.makedirs(cls.incl_dir, exist_ok=True)

        " Create 5 sub-folders "
        for subdir in ['1', '2', '3', '4', 'ignore']:
            os.makedirs(os.path.join(cls.incl_dir, subdir), exist_ok=True)

            " Each folder contains 5 text files "
            for name in range(5):
                # /path/to/project/tests/include/ignore/1.txt
                filepath: str = f'{TEST_DIR}/include/{subdir}/{name}.txt'

                " Each text file has about 5KiB of null data "
                with open(filepath, 'wb') as file:
                    file.seek(1024 - 1)
                    file.write(b"\0")

        " Instantiate backup profile from template provided by __init__.py"
        configuration: config.Configuration = config.Configuration(valid_config)
        cls.profile = backup.BackupProfile(configuration)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.incl_dir)
        shutil.rmtree(cls.profile.destination)

    def test_include_paths(self):
        """
        This test asserts the 'children' property of BackupProfile
        is a Set and all of them must be in absolute form.
        """
        self.assertTrue(isinstance(self.profile.children, set))

        for child in self.profile.children:
            self.assertTrue(os.path.isabs(child))

    def test_ignore_paths(self):
        """
        This test asserts the 'ignore' property of BackupProfile
        is a Set and all of them must be in absolute form.
        Additionally, 'ignore' paths must not present in 'children' property
        """
        self.assertTrue(isinstance(self.profile.ignore, set))

        for ignore in self.profile.ignore:
            self.assertTrue(os.path.isabs(ignore))
            self.assertNotIn(ignore, self.profile.children)

    def test_destination_path(self):
        """
        This test verifies that 'destination' property of BackupProfile
        is an absolute path.
        :return:
        """
        self.assertTrue(os.path.isabs(self.profile.destination))

        """
        Since path is defined in __init__.py, we can also perform
        check if relative path was parsed properly.
        """
        destination: str = os.path.join(TEST_DIR, 'backups')
        self.assertEqual(destination, self.profile.destination)

    def test_filename(self):
        """
        This test performs check on 'filename' property of BackupProfile
        An addition test to confirm that datetime is parsable
        """

        " This pattern is the result of 'time_format' defined in __init__.py"
        namepattern: str = r'\d{4}-\w{3}-\d{2} \d{2}-\d{2}-\d{6}.zstd'
        self.assertTrue(match(namepattern, self.profile.filename))

        date: str = self.profile.filename.split('.')[0]
        try:
            datetime.strptime(date, time_format)
        except:
            self.fail(f'{date} is not a valid date according to format {time_format}!')

    def test_length(self):
        """
        Get the total size of each individual file in the 'include' property
        :return:
        """
        self.assertTrue(len(self.profile) > 0)


class DeleteOlBackupTests(unittest.TestCase):
    path: str = os.path.join(TEST_DIR, 'backups')

    @classmethod
    def setUpClass(cls):
        # Create 'backups' folder, ignore if exists
        os.makedirs(cls.path, exist_ok=True)

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

        # Create empty .zstd files with names
        # are dates ranging from 1 to 40
        for day in [1, 2, 5, 10, 20, 30, 31, 35, 40]:
            filename = f'{TEST_DIR}/backups/{_get_date_ago(day)}.zstd'
            with open(filename, 'w'):
                pass

    @classmethod
    def tearDownClass(cls):
        """
        Remove 'tests/backups' folder
        """
        shutil.rmtree(cls.path)

    def test_del_old_backups(self):
        """
        This test performs deletion on various days
        (simulate different values of 'old_backups.retention')
        """
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
        backups: list[str] = scan_4_backup(self.path)

        for days, remain in values.items():
            backup.del_old_backups(backups, days)

            " Reload list after each deletion "
            backups = scan_4_backup(self.path)
            self.assertEqual(
                len(backups),
                remain,
                f'The remaining backups after deleting backups that are older than {days} days must be {remain}'
            )


if __name__ == '__main__':
    unittest.main()
