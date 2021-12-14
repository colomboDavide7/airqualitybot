######################################################
#
# Author: Davide Colombo
# Date: 14/12/21 20:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.file.parser.json_parser as parsertype


class TestJSONParser(unittest.TestCase):

    def test_successfully_parse_json(self):
        test_raw_json = '{"obj1": "val1", "obj2": {"k1": "v1"}}'
        parser = parsertype.JSONParser()
        actual = parser.parse(test_raw_json)
        expected = {"obj1": "val1", "obj2": {"k1": "v1"}}
        self.assertEqual(actual, expected)

    def test_system_exit_on_single_quotes_around_values(self):
        test_raw_json = '{"obj1": \'val1\'}'
        parser = parsertype.JSONParser()
        with self.assertRaises(SystemExit):
            parser.parse(test_raw_json)

    def test_system_exit_on_single_quotes_around_keys(self):
        test_raw_json = '{\'obj1\': "val1"}'
        parser = parsertype.JSONParser()
        with self.assertRaises(SystemExit):
            parser.parse(test_raw_json)

    def test_system_exit_on_bad_json(self):
        test_raw_json = '"obj1": "val1"'
        parser = parsertype.JSONParser()
        with self.assertRaises(SystemExit):
            parser.parse(test_raw_json)


if __name__ == '__main__':
    unittest.main()
