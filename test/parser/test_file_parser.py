#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:21
# @Description: unit test script
#
#################################################

import unittest
from airquality.parser.file_parser import FileParserFactory


class TestFileParser(unittest.TestCase):

    def setUp(self) -> None:
        self.json_parser = FileParserFactory.file_parser_from_file_extension("json")

    def test_successfully_parse_json_file(self):
        test_raw = '{"hello": "world"}'
        expected_parsed = {"hello": "world"}
        actual_parsed = self.json_parser.parse(test_raw)
        self.assertEqual(actual_parsed, expected_parsed)

    def test_system_exit_parser_factory(self):
        with self.assertRaises(SystemExit):
            FileParserFactory.file_parser_from_file_extension("xml")

    def test_system_exit_when_parse_invalid_json(self):
        test_raw = '{ "hello": "world" '
        with self.assertRaises(SystemExit):
            self.json_parser.parse(test_raw)

    def test_parse_empty_json_file(self):
        test_raw = "{}"
        expected_output = {}
        actual_output = self.json_parser.parse(test_raw)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
