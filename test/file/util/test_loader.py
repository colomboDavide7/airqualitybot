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
import file.json as jf


class TestFileLoader(unittest.TestCase):

    def tearDown(self) -> None:
        if 'connection' in os.environ:
            os.environ.pop("connection")
        if 'query_file' in os.environ:
            os.environ.pop('query_file')
        if 'directory_of_resources' in os.environ:
            os.environ.pop('directory_of_resources')

    def test_exit_on_missing_mandated_environment_properties(self):
        test_environment_path = "test/file/deprecated/.empty_env"
        with self.assertRaises(SystemExit):
            fl.load_environment_file(path_to_file=test_environment_path)

    def test_successfully_load_environment_file(self):
        test_environment_path = "test/file/deprecated/.test_env_ok"
        connection, query_file_path = fl.load_environment_file(path_to_file=test_environment_path)
        self.assertEqual(connection, "some_connection_string")
        self.assertEqual(query_file_path, "some_directory_name/some_file_name")

    def test_successfully_get_json_file(self):
        actual = fl.load_structured_file(file_path="test/file/deprecated/test_loader.json")
        self.assertEqual(actual.__class__, jf.JSONFile)


if __name__ == '__main__':
    unittest.main()
