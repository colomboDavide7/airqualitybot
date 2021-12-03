######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 17:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.file.util.reader as r


class TestFileReader(unittest.TestCase):

    def test_system_exit_on_invalid_path(self):
        with self.assertRaises(SystemExit):
            r.exit_if_path_does_not_exists_or_is_not_file(path="bad file path", caller_name="some_function")

    def test_system_exit_on_path_directory(self):
        with self.assertRaises(SystemExit):
            r.exit_if_path_does_not_exists_or_is_not_file(path="tests", caller_name="some_function")

    def test_successfully_open_read_close_file(self):
        actual = r.open_read_close_file('test/file/util/test_orc.txt')
        expected = "this is a simple test file.\nthis is line 2."
        self.assertEqual(actual, expected)

    def test_successfully_open_readlines_close_file(self):
        actual = r.open_readlines_close_file('test/file/util/test_orc.txt')
        expected = ["this is a simple test file.\n", "this is line 2."]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
