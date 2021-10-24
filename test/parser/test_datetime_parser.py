#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:07
# @Description: unit test script
#
#################################################
import unittest
from airquality.parser.datetime_parser import DatetimeParser
from airquality.picker import TIMESTAMP


class TestDatetimeParser(unittest.TestCase):


    def test_parse_atmotube_timestamp(self):

        time = "2021-07-12T09:44:00.000Z"
        expected_output = "2021-07-12 09:44:00"
        actual_output = DatetimeParser.parse_atmotube_timestamp(time)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_invalid_atmotube_timestamp(self):

        test_timestamp = "bad atmotube timestamp"
        with self.assertRaises(SystemExit):
            DatetimeParser._raise_system_exit_when_bad_timestamp_occurs(
                    ts = test_timestamp,
                    pattern = DatetimeParser.ATMOTUBE_DATETIME_PATTERN
            )


    def test_last_date_from_api_param(self):
        test_timestamp = "2021-10-11 09:44:00"
        expected_output = "2021-10-11"
        actual_output = DatetimeParser.date_from_last_atmotube_measure_timestamp(test_timestamp)
        self.assertEqual(actual_output, expected_output)


    def test_last_timestamp_from_packets(self):
        test_packet = [{f"{TIMESTAMP}": "ts1"}, {f"{TIMESTAMP}": "ts2"}, {f"{TIMESTAMP}": "ts3"}]
        expected_output = "ts3"
        actual_output = DatetimeParser.last_atmotube_measure_timestamp_from_packets(test_packet)
        self.assertEqual(actual_output, expected_output)


    def test_is_ts1_before_ts2(self):
        test_ts1 = "2021-10-01 09:43:59"
        test_ts2 = "2021-10-01 09:44:00"
        actual_output = DatetimeParser.is_ts1_before_ts2(ts1 = test_ts1, ts2 = test_ts2)
        self.assertTrue(actual_output)


    def test_error_when_timestamp_are_invalid(self):
        test_ts1 = "bad_timestamp"
        test_ts2 = "2021-10-01 09:44:00"
        with self.assertRaises(SystemExit):
            DatetimeParser.is_ts1_before_ts2(ts1 = test_ts1, ts2 = test_ts2)

        with self.assertRaises(SystemExit):
            DatetimeParser.is_ts1_before_ts2(ts1 = test_ts2, ts2 = test_ts1)


    def test_empty_timestamp_when_empty_packets(self):
        test_packets = []
        expected_output = ""
        actual_output = DatetimeParser.last_atmotube_measure_timestamp_from_packets(test_packets)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
