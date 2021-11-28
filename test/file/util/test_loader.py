######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 20:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import unittest
import airquality.file.util.loader as fl


class TestFileLoader(unittest.TestCase):

    def tearDown(self) -> None:
        if 'DBCONN' in os.environ:
            os.environ.pop("DBCONN")

    def test_exit_on_missing_database_connection_string_property(self):
        test_environment_path = "test/file/.empty_env"
        with self.assertRaises(SystemExit):
            fl.load_environment_file(file_path=test_environment_path, sensor_type="atmotube")

    def test_exit_on_missing_secret_purpleair_api_key(self):
        test_environment_path = "test/file/.missing_purpleair_env"
        with self.assertRaises(SystemExit):
            fl.load_environment_file(file_path=test_environment_path, sensor_type="purpleair")


if __name__ == '__main__':
    unittest.main()
