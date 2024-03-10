import unittest

from src.utils.type import verify


class TestTypeVerification(unittest.TestCase):

    def test_correct_values(self):
        str_type = verify('s', str)
        self.assertTrue(isinstance(str_type, str))
        self.assertEqual('s', str_type)

        int_type = verify(1, int)
        self.assertTrue(isinstance(int_type, int))
        self.assertEqual(1, int_type)

        float_type = verify(.7, float)
        self.assertTrue(isinstance(float_type, float))
        self.assertEqual(0.7, float_type)

        bool_type = verify(False, bool)
        self.assertTrue(isinstance(bool_type, bool))
        self.assertFalse(bool_type)

    def test_type_tuple(self):
        tup = (str, int, bool)

        try:
            str_type = verify('s', tup)
            self.assertTrue(isinstance(str_type, str))
            self.assertEqual('s', str_type)

            int_type = verify(1, tup)
            self.assertTrue(isinstance(int_type, int))
            self.assertEqual(1, int_type)

            bool_type = verify(False, tup)
            self.assertTrue(isinstance(bool_type, bool))
            self.assertFalse(bool_type)

        except TypeError as e:

            self.fail(e)

        self.assertRaises(TypeError, verify, (23.4, tup))

    def test_default_return(self):
        str_type = verify(1, str, default='string')
        self.assertTrue(isinstance(str_type, str))
        self.assertEqual('string', str_type)

    def test_force_cast(self):
        str_type = verify(1, str, force_cast=True)
        self.assertTrue(isinstance(str_type, str))
        self.assertEqual('1', str_type)


if __name__ == '__main__':
    unittest.main()
