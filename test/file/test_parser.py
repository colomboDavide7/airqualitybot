#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:21
# @Description: unit test script
#
#################################################
import unittest
import airquality.file.util.parser as txt


class TestFileParser(unittest.TestCase):

    def test_get_parser_class(self):
        obj_cls = txt.get_parser_class('json')
        self.assertEqual(obj_cls, txt.JSONParser)

        with self.assertRaises(SystemExit):
            txt.get_parser_class('bad file extension')

    def test_successfully_parse_json_file(self):
        test_raw = '{"hello": "world"}'
        expected_parsed = {"hello": "world"}
        actual_parsed = txt.JSONParser(test_raw).parse()
        self.assertEqual(actual_parsed, expected_parsed)

    def test_system_exit_when_parse_invalid_json(self):
        test_raw = '{ "hello": "world" '
        with self.assertRaises(SystemExit):
            txt.JSONParser(test_raw).parse()

    def test_parse_empty_json_file(self):
        test_raw = "{}"
        expected_output = {}
        actual_output = txt.JSONParser(test_raw).parse()
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
