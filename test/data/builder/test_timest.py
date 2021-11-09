#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:07
# @Description: unit test script
#
#################################################
import unittest
import airquality.data.builder.timest as tsmp


class TestTimestampBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_ts1 = tsmp.AtmotubeTimestamp("2021-10-11T09:44:00.000Z")
        self.atmotube_ts2 = tsmp.AtmotubeTimestamp("2018-01-01T00:00:00.000Z")
        self.thingspk_ts1 = tsmp.ThingspeakTimestamp("2021-09-04T17:35:44Z")
        self.thingspk_ts2 = tsmp.ThingspeakTimestamp("2020-07-14T14:05:09Z")

    def test_successfully_add_days_to_atmotube_timestamp(self):
        new_timest = self.atmotube_ts1.add_days(days=1)
        actual_output = new_timest.ts
        expected_output = "2021-10-12 09:44:00"
        self.assertEqual(actual_output, expected_output)

    def test_is_before_atmotube_timestamp(self):
        self.assertTrue(self.atmotube_ts2.is_before(self.atmotube_ts1))
        self.assertFalse(self.atmotube_ts1.is_before(self.atmotube_ts2))

    def test_system_exit_when_comparing_bad_type(self):
        with self.assertRaises(SystemExit):
            self.atmotube_ts1.is_before(self.thingspk_ts1)

    def test_system_exit_when_using_wrong_atmotube_timestamp_fmt(self):
        with self.assertRaises(SystemExit):
            tsmp.AtmotubeTimestamp(timestamp="bad timestamp fmt")

    def test_successfully_add_days_to_thingspeak_timestamp(self):
        new_timest = self.thingspk_ts1.add_days(days=10)
        actual_output = new_timest.ts
        expected_output = "2021-09-14 17:35:44"
        self.assertEqual(actual_output, expected_output)

    def test_is_before_thingspeak_timestamp(self):
        self.assertTrue(self.thingspk_ts2.is_before(self.thingspk_ts1))
        self.assertFalse(self.thingspk_ts1.is_before(self.thingspk_ts2))

    def test_system_exit_when_using_wrong_thingspeak_timestamp_fmt(self):
        with self.assertRaises(SystemExit):
            tsmp.ThingspeakTimestamp(timestamp="bad timestamp fmt")

    def test_system_exit_when_comparing_thingspeak_timestamp_to_invalid_type(self):
        with self.assertRaises(SystemExit):
            self.thingspk_ts1.is_before(self.atmotube_ts1)





    # def test_successfully_parse_atmotube_timestamp(self):
    #     """Test the conversion of an Atmotube timestamp to SQL timestamp."""
    #
    #     test_ts = "2021-07-12T09:44:00.000Z"
    #     expected_output = "2021-07-12 09:44:00"
    #     actual_output = DatetimeParser.atmotube_to_sqltimestamp(test_ts)
    #     self.assertEqual(actual_output, expected_output)
    #
    # def test_system_exit_when_invalid_atmotube_timestamp(self):
    #     """Test SystemExit when try to convert invalid atmotube timestamp."""
    #
    #     test_ts = "bad atmotube timestamp"
    #     with self.assertRaises(SystemExit):
    #         DatetimeParser.atmotube_to_sqltimestamp(ts=test_ts)
    #
    # def test_successfully_extract_date_from_sqltimestamp(self):
    #     """Test extracting data from SQL timestamp."""
    #
    #     test_ts = "2021-10-11 09:44:00"
    #     expected_output = "2021-10-11"
    #     actual_output = DatetimeParser.sqltimestamp_date(ts=test_ts)
    #     self.assertEqual(actual_output, expected_output)
    #
    # def test_successfully_verify_ts2_after_ts1(self):
    #     """Test sqltimestamp comparison."""
    #
    #     test_ts1 = "2021-10-01 09:43:59"
    #     test_ts2 = "2021-10-01 09:44:00"
    #     self.assertTrue(DatetimeParser.is_ts2_after_ts1(ts1=test_ts1, ts2=test_ts2))
    #     self.assertFalse(DatetimeParser.is_ts2_after_ts1(ts1=test_ts2, ts2=test_ts2))
    #
    # def test_from_date_to_string(self):
    #     test_date = datetime.datetime(year=2019, month=1, day=1)
    #     expected_output = "2019-01-01 00:00:00"
    #     actual_output = DatetimeParser.datetime2string(ts=test_date)
    #     self.assertEqual(actual_output, expected_output)
    #
    # def test_from_string_to_date(self):
    #     test_date_string = "2019-01-01 00:00:00"
    #     date_obj = DatetimeParser.string2datetime(datetime_string=test_date_string)
    #     self.assertIsInstance(date_obj, datetime.date)
    #
    # def test_add_days_to_date(self):
    #     test_starting_date = datetime.datetime(year=2019, month=1, day=1)
    #     expected_output = datetime.datetime(year=2019, month=1, day=11)
    #     actual_output = DatetimeParser.add_days_to_datetime(ts=test_starting_date, days=10)
    #     self.assertEqual(actual_output, expected_output)
    #     self.assertIsInstance(actual_output, datetime.date)
    #
    # def test_successfully_convert_timestamp_from_thingspeak_to_sql(self):
    #     test_ts = "2021-10-27T05:36:59Z"
    #     expected_output = "2021-10-27 05:36:59"
    #     actual_output = DatetimeParser.thingspeak_to_sqltimestamp(ts=test_ts)
    #     self.assertEqual(actual_output, expected_output)
    #
    # def test_system_exit_while_parsing_thingspeak_timestamp(self):
    #     test_ts = "bad_timestamp"
    #     with self.assertRaises(SystemExit):
    #         DatetimeParser.thingspeak_to_sqltimestamp(ts=test_ts)
    #
    # def test_add_seconds_to_datetime(self):
    #     test_starting_datetime = datetime.datetime(year=2019, month=7, day=9, second=4)
    #     expected_output = datetime.datetime(year=2019, month=7, day=9, second=7)
    #     actual_output = DatetimeParser.add_seconds_to_datetime(ts=test_starting_datetime, seconds=3)
    #     self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
