#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 09:20
# @Description: unit test script
#
#################################################


import unittest
from airquality.picker.json_param_picker import JSONParamPicker


class TestJSONParamPicker(unittest.TestCase):

    def test_successfully_pick_parameter(self):
        test_json = {"key1": {"key2": "val2", "key3": "val3"}}
        test_path2key = ["key1", "key2"]
        expected_output = "val2"

        actual_output = JSONParamPicker.pick_parameter(parsed_json=test_json, path2key=test_path2key)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_path2key_is_empty_purpleair_json_picker(self):
        test_json = {"key1": {"key2": "val2", "key3": "val3"}}
        test_path2key = []

        with self.assertRaises(SystemExit):
            JSONParamPicker.pick_parameter(parsed_json=test_json, path2key=test_path2key)

    def test_system_exit_when_parsed_json_is_empty_purpleair_json_picker(self):
        test_json = {}
        test_path2key = ["some_key", "some_key2"]

        with self.assertRaises(SystemExit):
            JSONParamPicker.pick_parameter(parsed_json=test_json, path2key=test_path2key)

    def test_system_exit_when_invalid_key_in_path2key_purpleair_json_picker(self):
        test_json = {"key1": {"key2": "val2", "key3": "val3"}}
        test_path2key = ["key1", "bad_key"]

        with self.assertRaises(SystemExit):
            JSONParamPicker.pick_parameter(parsed_json=test_json, path2key=test_path2key)

        test_path2key = ["bad_key"]
        with self.assertRaises(SystemExit):
            JSONParamPicker.pick_parameter(parsed_json=test_json, path2key=test_path2key)


if __name__ == '__main__':
    unittest.main()
