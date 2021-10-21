#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 11:38
# @Description: Test script for database response parser.
#
#################################################
import unittest
from airquality.parser.db_resp_parser import DatabaseResponseParser


class TestDatabaseResponseParser(unittest.TestCase):
    """Test class for DatabaseResponseParser."""

    def test_parse_key_val_response(self):
        """
        Test the correct conversion from list of key-value tuples to dictionary.

        If response is empty, empty dictionary must be returned.
        """

        response = []
        expected_output = {}
        actual_output = DatabaseResponseParser.parse_key_val_response(response)
        self.assertEqual(actual_output, expected_output)

        response = [("api_key", "value"),
                    ("mac", "value"),
                    ("order", "desc")]

        expected_output = {"api_key": "value", "mac": "value", "order": "desc"}
        actual_output = \
            DatabaseResponseParser.parse_key_val_response(response)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_key_val_response(self):
        """Test SystemExit when tuple has length not equal to 2."""
        response = [(1, ), (2, ), (3, )]
        with self.assertRaises(SystemExit):
            DatabaseResponseParser.parse_key_val_response(response)

        response = [(1, 2, 3)]
        with self.assertRaises(SystemExit):
            DatabaseResponseParser.parse_key_val_response(response)

    def test_parse_one_field_response(self):
        """
        Test correct conversion from a list of one-element tuple into a list.
        """
        response = [(1, ), (2, ), (3, )]
        expected_output = [1, 2, 3]
        actual_output = DatabaseResponseParser.parse_one_field_response(response)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_parse_one_field(self):
        """Test SystemExit when try to parse list of more-than-one-element
        tuples."""

        response = [("api_key", "value"),
                    ("mac", "value"),
                    ("order", "desc")]

        with self.assertRaises(SystemExit):
            DatabaseResponseParser.parse_one_field_response(response)



if __name__ == '__main__':
    unittest.main()
