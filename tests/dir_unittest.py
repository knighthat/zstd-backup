import os
import shutil
import unittest
from datetime import datetime, timedelta

from src import backup, dir


class DirTestCase(unittest.TestCase):

    @classmethod
    def tearDown(cls) -> None:
        """
        Clean up files and folders that were created during tests
        """

        # List of dirs or files that were created during tests
        created: list[str] = [
            'folder1',  # From test_folder_exist()
            'file1',  # From test_file_exist()
            'dates'  # From test_scan_4_backup()
        ]

        for name in created:
            if os.path.exists(name):
                if os.path.isdir(name):
                    shutil.rmtree(name)
                elif os.path.isfile(name):
                    os.remove(name)

    def test_folder_exist(self):
        self.assertEqual(dir.folder_exist('folder1'), dir.ReturnCode.NOT_EXIST, 'This folder is not supposed to exist!')

        # Create an empty FILE named 'folder1'
        with open('folder1', 'w'):
            pass
        self.assertEqual(dir.folder_exist('folder1'), dir.ReturnCode.WRONG_TYPE, '\"folder1\" is supposed to be a file!')
        os.remove('folder1')

        # Create an empty DIRECTORY named 'folder1'
        os.mkdir('folder1')
        self.assertEqual(dir.folder_exist('folder1'), dir.ReturnCode.EXIST, 'Directory \"folder1\" does not exist!')
        shutil.rmtree('folder1')

    def test_file_exist(self):
        self.assertEqual(dir.file_exist('file1'), dir.ReturnCode.NOT_EXIST, 'File \"file1\" is not supposed to exist!')

        # Create an empty DIRECTORY named 'file1'
        os.mkdir('file1')
        self.assertEqual(dir.file_exist('file1'), dir.ReturnCode.WRONG_TYPE, '\"file1\" is supposed to be a folder!')
        shutil.rmtree('file1')

        # Create an empty FILE named 'file1'
        with open('file1', 'w'):
            pass
        self.assertEqual(dir.file_exist('file1'), dir.ReturnCode.EXIST, 'File \"file1\" does not exist!')
        os.remove('file1')

    def test_scan_4_backup(self):
        # Create a list consists of dates from today to 45 days prior.
        dates: list[datetime] = []

        # This for-loop will go from 45 to 0
        # then it will subtract the date from today
        # For example, i=2 will result in the
        # date of 2 days before.
        for i in range(45, -1, -1):
            dates.append(backup.today - timedelta(days=i))

        # A second list that stores dates as string
        # with Zstandard file extension.
        date_strings: list[str] = []

        # Make a folder and put all files into it
        os.mkdir('dates')
        for date in dates:
            # Convert datetime obj to string follow format defined in 'backup.time_format'
            filename = f'{date.strftime(backup.time_format)}.zstd'
            filepath = f'dates/{filename}'
            date_strings.append(filepath)

            with open(filepath, 'w'):
                pass

        self.assertCountEqual(dir.scan_4_backup('dates'), date_strings, 'Mismatch backup list')
        shutil.rmtree('dates')

    def test_abspath(self):
        parent = os.path.abspath(os.pardir)
        filepath = 'path/to/file'

        # This scenario will test the conversion of '~' character.
        # The '~' character must be converted into the value of $HOME
        # and the result must be an absolute path.
        case1 = dir.abspath(f'~/{filepath}')
        xpt_case1 = f'{os.path.expanduser("~")}/{filepath}'
        self.assertTrue(os.path.isabs(case1), f'{case1} must be an absolute path!')
        self.assertTrue(os.path.isabs(xpt_case1), f'{xpt_case1} must be an absolute path!')
        self.assertEqual(xpt_case1, case1)

        # This scenario tests the conversion of '.' (current directory) character.
        # The '.' character must the converted into the project's directory (zstd_backup.py's dir)
        # and the result must be an absolute path.
        case2 = dir.abspath(f'./{filepath}')
        xpt_case2 = f'{parent}/{filepath}'
        self.assertTrue(os.path.isabs(case2), f'{case2} must be an absolute path!')
        self.assertTrue(os.path.isabs(xpt_case2), f'{xpt_case2} must be an absolute path!')
        self.assertEqual(xpt_case2, case2)

        # This scenario will not convert '.' character because it's a file
        # starts with a dot (signal for hidden file on Linux machine).
        # This relative path will be appended to the project's directory
        # (zstd_backup.py's dir) and the result must be an absolute path
        case3 = dir.abspath('.file')
        xpt_case3 = f'{parent}/.file'
        self.assertTrue(os.path.isabs(case3), f'{case3} must be an absolute path!')
        self.assertTrue(os.path.isabs(xpt_case3), f'{xpt_case3} must be an absolute path!')
        self.assertEqual(xpt_case3, case3)

        # This scenario asserts the path will not be converted if
        # it's already in absolute form.
        xpt_case4 = f'{parent}/file'
        case4 = dir.abspath(xpt_case4)
        self.assertTrue(os.path.isabs(case4), f'{case4} must be an absolute path!')
        self.assertTrue(os.path.isabs(xpt_case4), f'{xpt_case4} must be an absolute path!')
        self.assertEqual(xpt_case3, case3)

        # This scenario confirms ValueError exception will be thrown
        # if the file contains invalid character in its path
        with self.assertRaises(ValueError):
            dir.abspath(f':/null')


if __name__ == '__main__':
    unittest.main()
