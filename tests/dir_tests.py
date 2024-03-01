import os
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from shutil import rmtree

from src import PROJECT_DIR, time_format, today
from src.dir import abspath, ReturnCode, folder_exist, scan_4_backup
from tests import TEST_DIR


class FileAndFolderTest(unittest.TestCase):

    def test_folder_exist(self):
        path: str = os.path.join(TEST_DIR, 'folder1')

        self.assertEqual(folder_exist(path), ReturnCode.NOT_EXIST, 'This folder is not supposed to exist!')

        # Create an empty FILE named 'folder1'
        with open(path, 'w'):
            pass
        self.assertEqual(folder_exist(path), ReturnCode.WRONG_TYPE, '\"folder1\" is supposed to be a file!')
        os.remove(path)

        # Create an empty DIRECTORY named 'folder1'
        os.mkdir(path)
        self.assertEqual(folder_exist(path), ReturnCode.EXIST, 'Directory \"folder1\" does not exist!')
        rmtree(path)


class BackupScannerTest(unittest.TestCase):
    path: str = os.path.join(TEST_DIR, 'dates')
    dates: set[str] = set()

    @classmethod
    def setUp(cls):
        os.makedirs(cls.path, exist_ok=True)

        # This for-loop will go from 45 to 0
        # then it will subtract the date from today
        # For example, i=2 will result in the
        # date of 2 days before.
        for i in range(45, -1, -1):
            date: datetime = today - timedelta(days=i)

            filename: str = f'{date.strftime(time_format)}.zstd'
            filepath: str = os.path.join(cls.path, filename)
            cls.dates.add(filepath)

            with open(filepath, 'w'):
                pass

    @classmethod
    def tearDown(cls):
        rmtree(cls.path)

    def test_scan_4_backup(self):
        scanned: list[str] = scan_4_backup(self.path)
        self.assertCountEqual(self.dates, scanned)


class AbsPathTest(unittest.TestCase):

    def test_absolute_path(self):
        """
        This scenario asserts the path will not be
        converted because it's already in absolute form.
        """
        path: str = Path('/path/to/file').__str__()
        result: str = abspath(path)
        self.assertEqual(path, result)
        self.assertTrue(os.path.isabs(result))

    def test_dot_relative_path(self):
        """
        This scenario tests the conversion of '.' (current directory) character.
        The '.' character must the converted into the project's directory
        (main.py's dir) and the result must be an absolute path.
        """
        expected: str = Path(f'{PROJECT_DIR}/rel/path').__str__()
        result: str = abspath(Path('./rel/path').__str__())
        self.assertEqual(expected, result)
        self.assertTrue(os.path.isabs(result))

    def test_dot_file_path(self):
        """
        This scenario will not convert '.' character because it's a file
        starts with a dot (signal for hidden file on Linux machine).
        This relative path will be appended to the project's directory
        (main.py's dir) and the result must be an absolute path
        """
        expected: str = Path(f'{PROJECT_DIR}/.dotfile').__str__()
        result: str = abspath('.dotfile')
        self.assertEqual(expected, result)
        self.assertTrue(os.path.isabs(result))

    def test_user_home_path(self):
        """
        This scenario will test the conversion of '~' character.
        The '~' character must be converted into the value of $HOME
        and the result must be an absolute path.
        """
        expected: str = Path(f'{os.path.expanduser("~")}/directory').__str__()
        result: str = abspath(Path('~/directory').__str__())
        self.assertEqual(result, expected)
        self.assertTrue(os.path.isabs(result))

    def test_other_cases(self):
        """
        This scenario will append project's dir (main.py's dir)
        to the beginning of the path to make it absolute.
        """
        expected: str = Path(f'{PROJECT_DIR}/;/rel/path').__str__()
        result: str = abspath(';/rel/path')
        self.assertEqual(result, expected)
        self.assertTrue(os.path.isabs(result))


if __name__ == '__main__':
    unittest.main()
