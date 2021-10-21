#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:21
# @Description: Script for testing resources parsing behaviour
#
#################################################

import unittest
from airquality.parser.file_parser import FileParserFactory

class TestFileParser(unittest.TestCase):

    def setUp(self) -> None:
        self.json_parser = FileParserFactory.file_parser_from_file_extension("json")

    def test_parse_json_file(self):
        """Test method for parsing content."""

        test_raw = '{"hello": "world"}'
        expected_parsed = {"hello": "world"}
        actual_parsed = self.json_parser.parse(test_raw)
        self.assertEqual(actual_parsed, expected_parsed)

    def test_system_exit_parser_factory(self):
        """
        Test SystemExit when not supported file extension is passed as argument."""

        with self.assertRaises(SystemExit):
            FileParserFactory.file_parser_from_file_extension("xml")

    def test_JSONDecodeError_parse(self):
        """Test JSONDecodeError while parsing json file."""

        test_raw = '{ "hello": "world" '
        with self.assertRaises(SystemExit):
            self.json_parser.parse(test_raw)


if __name__ == '__main__':
    unittest.main()
