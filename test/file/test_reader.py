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
            r.open_read_close_file(path="bad file path")

    def test_system_exit_on_path_directory(self):
        with self.assertRaises(SystemExit):
            r.open_read_close_file("tests")

    def test_successfully_open_read_close_file(self):
        r.open_read_close_file('test/file/test_orc.txt')


if __name__ == '__main__':
    unittest.main()
