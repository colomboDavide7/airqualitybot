#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 11:38
# @Description: unit test script
#
#################################################
import unittest
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.constants.shared_constants import EMPTY_LIST, EMPTY_DICT


class TestDatabaseAnswerParser(unittest.TestCase):


    def test_parse_key_val_answer(self):
        """Test the correct conversion from list of key-value tuples to dictionary."""

        test_answer = EMPTY_LIST
        expected_output = EMPTY_DICT
        actual_output = DatabaseAnswerParser.parse_key_val_answer(test_answer)
        self.assertEqual(actual_output, expected_output)

        test_answer = [("api_key", "value"), ("mac", "value"), ("order", "desc")]
        expected_output = {"api_key": "value", "mac": "value", "order": "desc"}
        actual_output = DatabaseAnswerParser.parse_key_val_answer(test_answer)
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_key_val_answer(self):
        """Test SystemExit when tuple has length not equal to 2."""

        answer = [(1,), (2,), (3,)]
        with self.assertRaises(SystemExit):
            DatabaseAnswerParser.parse_key_val_answer(answer)

        answer = [(1, 2, 3)]
        with self.assertRaises(SystemExit):
            DatabaseAnswerParser.parse_key_val_answer(answer)


    def test_parse_one_field_answer(self):
        """Test correct conversion from a list of one-element tuple into a list."""

        answer = [(1,), (2,), (3,)]
        expected_output = [1, 2, 3]
        actual_output = DatabaseAnswerParser.parse_single_attribute_answer(answer)
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_parse_one_field_answer(self):
        """Test SystemExit when try to parse list of more-than-one-element tuples."""

        answer = [("api_key", "value"), ("mac", "value"), ("order", "desc")]
        with self.assertRaises(SystemExit):
            DatabaseAnswerParser.parse_single_attribute_answer(answer)


if __name__ == '__main__':
    unittest.main()
