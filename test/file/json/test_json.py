######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 21:02
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.file.json as filetype


class TestJSONFile(unittest.TestCase):

    PATH_TO_TEST_FILE = "test/file/json/test_json.json"

    def test_recursive_search(self):
        test_path_to_object = ["obj2"]
        actual = filetype.JSONFile(path_to_file=TestJSONFile.PATH_TO_TEST_FILE, path_to_object=test_path_to_object)
        self.assertEqual(actual.k1, "v1")
        self.assertEqual(actual.k2, "v2")

    def test_system_exit_when_key_error_occurs(self):
        test_path_to_object = ["obj2"]
        actual = filetype.JSONFile(path_to_file=TestJSONFile.PATH_TO_TEST_FILE, path_to_object=test_path_to_object)
        with self.assertRaises(SystemExit):
            print(actual.bad_attribute)

    def test_system_exit_when_type_error_occurs(self):
        test_path_to_object = ["obj2", "k1"]
        actual = filetype.JSONFile(path_to_file=TestJSONFile.PATH_TO_TEST_FILE, path_to_object=test_path_to_object)
        with self.assertRaises(SystemExit):
            print(actual.some_attribute_name)

    def test_system_exit_when_path_to_object_is_wrong(self):
        test_path_to_object = ["bad_object"]
        with self.assertRaises(SystemExit):
            filetype.JSONFile(path_to_file=TestJSONFile.PATH_TO_TEST_FILE, path_to_object=test_path_to_object)


if __name__ == '__main__':
    unittest.main()
