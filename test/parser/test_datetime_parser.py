#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:07
# @Description: unit test script
#
#################################################
import unittest
from airquality.parser.datetime_parser import DatetimeParser


class TestDatetimeParser(unittest.TestCase):


    def test_successfully_parse_atmotube_timestamp(self):
        """Test the conversion of an Atmotube timestamp to SQL timestamp."""

        test_ts = "2021-07-12T09:44:00.000Z"
        expected_output = "2021-07-12 09:44:00"
        actual_output = DatetimeParser.atmotube_to_sqltimestamp(test_ts)
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_when_invalid_atmotube_timestamp(self):
        """Test SystemExit when try to convert invalid atmotube timestamp."""

        test_ts = "bad atmotube timestamp"
        with self.assertRaises(SystemExit):
            DatetimeParser.atmotube_to_sqltimestamp(ts = test_ts)


    def test_successfully_extract_date_from_sqltimestamp(self):
        """Test extracting data from SQL timestamp."""

        test_ts = "2021-10-11 09:44:00"
        expected_output = "2021-10-11"
        actual_output = DatetimeParser.sqltimestamp_date(ts = test_ts)
        self.assertEqual(actual_output, expected_output)


    def test_successfully_verify_ts2_after_ts1(self):

        test_ts1 = "2021-10-01 09:43:59"
        test_ts2 = "2021-10-01 09:44:00"
        self.assertTrue(DatetimeParser.is_ts2_after_ts1(ts1 = test_ts1, ts2 = test_ts2))
        self.assertFalse(DatetimeParser.is_ts2_after_ts1(ts1 = test_ts2, ts2 = test_ts2))


if __name__ == '__main__':
    unittest.main()
