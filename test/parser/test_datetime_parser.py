#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:07
# @Description: unit test script
#
#################################################
import datetime
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
        """Test sqltimestamp comparison."""

        test_ts1 = "2021-10-01 09:43:59"
        test_ts2 = "2021-10-01 09:44:00"
        self.assertTrue(DatetimeParser.is_ts2_after_ts1(ts1 = test_ts1, ts2 = test_ts2))
        self.assertFalse(DatetimeParser.is_ts2_after_ts1(ts1 = test_ts2, ts2 = test_ts2))


    def test_from_date_to_string(self):

        test_date = datetime.datetime(year = 2019, month = 1, day = 1)
        expected_output = "2019-01-01 00:00:00"
        actual_output = DatetimeParser.datetime2string(ts = test_date)
        self.assertEqual(actual_output, expected_output)


    def test_from_string_to_date(self):

        test_date_string = "2019-01-01 00:00:00"
        date_obj = DatetimeParser.string2datetime(datetime_string = test_date_string)
        self.assertIsInstance(date_obj, datetime.date)


    def test_add_days_to_date(self):

        test_starting_date = datetime.datetime(year = 2019, month = 1, day = 1)
        expected_output = datetime.datetime(year = 2019, month = 1, day = 11)
        actual_output = DatetimeParser.add_days_to_datetime(ts = test_starting_date, days = 10)
        self.assertEqual(actual_output, expected_output)
        self.assertIsInstance(actual_output, datetime.date)


    def test_successfully_convert_timestamp_from_thingspeak_to_sql(self):

        test_ts = "2021-10-27T05:36:59Z"
        expected_output = "2021-10-27 05:36:59"
        actual_output = DatetimeParser.thingspeak_to_sqltimestamp(ts = test_ts)
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_while_parsing_thingspeak_timestamp(self):

        test_ts = "bad_timestamp"
        with self.assertRaises(SystemExit):
            DatetimeParser.thingspeak_to_sqltimestamp(ts = test_ts)


if __name__ == '__main__':
    unittest.main()
