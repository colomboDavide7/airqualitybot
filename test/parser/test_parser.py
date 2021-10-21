#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:21
# @Description: Script for testing resources parsing behaviour
#
#################################################

import unittest
from airquality.parser.parser import JSONParser, ParserFactory

class TestParser(unittest.TestCase):

    def setUp(self) -> None:
        self.json_parser = ParserFactory.make_parser_from_extension_file("json")

    def test_type_error_in_parser_factory(self):
        """Test TypeError when not supported file extension
        is passed as argument."""

        with self.assertRaises(SystemExit):
            ParserFactory.make_parser_from_extension_file("xml")

    def test_parse_json(self):
        """Test method for parsing content."""

        test_raw = '{"hello": "world"}'
        expected_parsed = {"hello": "world"}
        actual_parsed = self.json_parser.parse(test_raw)
        self.assertEqual(actual_parsed, expected_parsed)

    def test_JSONDecodeError_parse(self):
        """Test JSONDecodeError while parsing json file."""

        test_raw = '{ "hello": "world" '
        with self.assertRaises(SystemExit):
            self.json_parser.parse(test_raw)


if __name__ == '__main__':
    unittest.main()
