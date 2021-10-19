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

    def test_new_parser(self):
        """Test method for the creation of a new Parser object."""
        json_parser = ParserFactory.make_parser_from_extension_file(
                file_extension = "json", raw_content = '{ "hello": "world" }'
        )
        self.assertIsInstance(json_parser, JSONParser)
        self.assertIsNotNone(json_parser)

    def test_type_error_in_parser_factory(self):
        """Test TypeError when not supported file extension
        is passed as argument."""
        with self.assertRaises(TypeError):
            ParserFactory.make_parser_from_extension_file("xml", "")

    def test_parse_json(self):
        """Test method for parsing content."""
        json_parser = ParserFactory.make_parser_from_extension_file(
                file_extension = "json", raw_content = '{ "hello": "world" }'
        )
        expected_parsed = {"hello": "world"}
        actual_parsed = json_parser.parse()
        self.assertEqual(actual_parsed, expected_parsed)

    def test_value_error_when_setting_raw(self):
        """
        Test ValueError when try to set 'raw' content from outside.
        """
        json_parser = ParserFactory.make_parser_from_extension_file(
                file_extension = "json", raw_content = '{ "hello": "world" }'
        )

        with self.assertRaises(ValueError):
            json_parser.raw = "Cannot set value"



if __name__ == '__main__':
    unittest.main()
