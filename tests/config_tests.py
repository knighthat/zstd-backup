import unittest
from logging import DEBUG

from src.config import OldBackupSettings, ZstdArguments, Configuration
from tests import TEST_DIR, valid_config


class OldBackupSettingsTest(unittest.TestCase):

    def test_default_values(self):
        """
        This function will test whether the default values
        are applied if invalid values are provided as the
        parameters.
        """
        invalid_values: dict = {
            'keep': '1',
            'retention': '2',
            'remove_old_backups_for_space': 'False',
            'aggressive': 'True'
        }
        configuration = OldBackupSettings(invalid_values)
        self.assertNotEqual(1, configuration.keep)
        self.assertNotEqual(2, configuration.retention)
        self.assertFalse(configuration.del_old_4_space)
        self.assertFalse(configuration.aggressive)

    def test_valid_values(self):
        """
        This function tests whether new values are applied
        if correct values are provided as the parameters.
        """
        values: dict = {
            'keep': 1,
            'retention': 2,
            'remove_old_backups_for_space': False,
            'aggressive': True
        }
        configuration = OldBackupSettings(values)
        self.assertEqual(1, configuration.keep)
        self.assertEqual(2, configuration.retention)
        self.assertFalse(configuration.del_old_4_space)
        self.assertTrue(configuration.aggressive)


class ZstdArgumentsTest(unittest.TestCase):

    def test_default_values(self):
        """
        This function will test whether the default values
        are applied if invalid values are provided as the
        parameters.
        """
        invalid_values: dict = {
            'level': '1',
            'threads': '2'
        }
        configuration = ZstdArguments(invalid_values)
        self.assertNotEqual(1, configuration.level)
        self.assertNotEqual(2, configuration.threads)

    def test_valid_values(self):
        """
        This function tests whether new values are applied
        if correct values are provided as the parameters.
        """
        values: dict = {
            'level': 1,
            'threads': 2
        }
        configuration = ZstdArguments(values)
        self.assertEqual(1, configuration.level)
        self.assertEqual(2, configuration.threads)


class ConfigurationTest(unittest.TestCase):
    incl_dir: str = f'{TEST_DIR}/include'
    config: Configuration

    @classmethod
    def setUpClass(cls):
        cls.config = Configuration(valid_config)

    def test_log_level(self):
        self.assertEqual(DEBUG, self.config.log_level)

    def test_include_paths(self):
        """
        This test confirms all paths should be present
        """
        for subdir in ['1', '2', '3', '4']:
            filepath: str = f'./tests/include/{subdir}'
            self.assertIn(filepath, self.config.include)

    def test_destination(self):
        """
        This test performs check whether destination is imported correctly
        """
        self.assertEqual('./tests/backups', self.config.destination)

    def test_ignore_paths(self):
        """
        This test asserts ignore path is correctly imported
        """
        self.assertIn('./tests/include/ignore', self.config.ignore_paths)

    def test_old_backup_settings(self):
        """
        Assert 'old_backups' properties
        """
        self.assertEqual(1, self.config.old_backup_settings.keep)
        self.assertEqual(2, self.config.old_backup_settings.retention)
        self.assertFalse(self.config.old_backup_settings.del_old_4_space)
        self.assertTrue(self.config.old_backup_settings.aggressive)

    def test_zstd_arguments(self):
        """
        Assert 'zstd_arguments' properties
        """
        self.assertEqual(1, self.config.zstd_arguments.level)
        self.assertEqual(2, self.config.zstd_arguments.threads)

    def test_fatal_include_configuration(self):
        """
        Parser must throw TypeError when invalid
        type of 'include' is provided
        """
        invalid_include = valid_config.copy()
        invalid_include['include'] = 2
        self.assertRaises(TypeError, Configuration, invalid_include)

    def test_fatal_destination_configuration(self):
        """
        Parser must throw TypeError when invalid
        type of 'destination' is provided
        """
        invalid_destination = valid_config.copy()
        invalid_destination['destination'] = True
        self.assertRaises(TypeError, Configuration, invalid_destination)

    def test_fatal_ignore_configuration(self):
        """
        Parser must throw TypeError when invalid
        type of 'ignore' is provided
        """
        invalid_ignore = valid_config.copy()
        invalid_ignore['ignore'] = 1
        self.assertRaises(TypeError, Configuration, invalid_ignore)

    def test_acceptable_include(self):
        """
        'include' accepts string as valid value.
        This test asserts no TypeError raises during this process
        """
        valid_include = valid_config.copy()
        valid_include['include'] = '/include/this/path'
        try:
            configuration: Configuration = Configuration(valid_include)
            self.assertIn('/include/this/path', configuration.include)
        except TypeError:
            self.fail('"include" string was not parsed properly!')

    def test_acceptable_ignore(self):
        """
        'ignore' accepts string as valid value.
        This test asserts no TypeError raises during this process
        """
        valid_ignore = valid_config.copy()
        valid_ignore['ignore'] = '/ignore/this/path'
        try:
            configuration: Configuration = Configuration(valid_ignore)
            self.assertIn('/ignore/this/path', configuration.ignore_paths)
        except TypeError:
            self.fail('"ignore" string was not parsed properly!')


if __name__ == '__main__':
    unittest.main()
