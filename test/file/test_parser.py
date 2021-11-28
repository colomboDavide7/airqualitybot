#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:21
# @Description: unit test script
#
#################################################
import unittest
import airquality.file.util.parser as parser


class TestFileParser(unittest.TestCase):

    def setUp(self) -> None:
        self.json_parser = parser.JSONParser()

    def test_get_parser_class(self):
        obj_cls = parser.get_file_parser('json')
        self.assertEqual(obj_cls.__class__, parser.JSONParser)

        with self.assertRaises(SystemExit):
            parser.get_file_parser('bad file extension')

    def test_successfully_parse_json_file(self):
        test_raw = '{"hello": "world"}'
        expected_parsed = {"hello": "world"}
        actual_parsed = self.json_parser.parse(test_raw)
        self.assertEqual(actual_parsed, expected_parsed)

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
