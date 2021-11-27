######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 17:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import unittest
import airquality.file.util.loader as fl


class TestLoader(unittest.TestCase):

    def tearDown(self) -> None:
        if 'DBCONN' in os.environ:
            os.environ.pop('DBCONN')

    def test_system_exit_on_missing_required_properties_in_environment_file(self):
        with self.assertRaises(SystemExit):
            fl.load_environment_file(file_path='test/file/.bad_env', sensor_type='atmotube')

    def test_system_exit_on_missing_purpleair_api_key(self):
        with self.assertRaises(SystemExit):
            fl.load_environment_file(file_path='test/file/.env_without_purp_key', sensor_type='purpleair')


if __name__ == '__main__':
    unittest.main()
