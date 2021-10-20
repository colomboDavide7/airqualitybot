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


    def test_parse_key_val_response(self):
        """
        Test the correct conversion from list of key-value tuples to dictionary.
        """
        response = [("api_key", "value"),
                    ("mac", "value"),
                    ("order", "desc")]

        expected_output = {"api_key": "value", "mac": "value", "order": "desc"}
        actual_output = \
            DatabaseResponseParser.parse_key_val_response(response)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_key_val_response(self):
        """Test SystemExit when tuple has length not equal to 2."""
        response = [('1'), ('2'), ('3')]

        with self.assertRaises(SystemExit):
            DatabaseResponseParser.parse_key_val_response(response)



if __name__ == '__main__':
    unittest.main()
