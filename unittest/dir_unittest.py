import os
import shutil
import unittest
from datetime import datetime, timedelta

import backup
import dir


class DirTestCase(unittest.TestCase):

    @classmethod
    def tearDown(self) -> None:
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

        case1 = f'~/{filepath}'
        xpt_case1 = f'{os.path.expanduser("~")}/{filepath}'
        self.assertEqual(xpt_case1, dir.abspath(case1))

        case2 = f'./{filepath}'
        xpt_case2 = f'{parent}/{filepath}'
        self.assertEqual(xpt_case2, dir.abspath(case2))

        xpt_case3 = f'{parent}/.file'
        self.assertEqual(xpt_case3, dir.abspath('.file'))


if __name__ == '__main__':
    unittest.main()
