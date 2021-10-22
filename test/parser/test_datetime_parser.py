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
        expected_output = "2021-07-12 09:44:00.000"
        actual_output = DatetimeParser.parse_atmotube_timestamp(time)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_while_parsing_atmotube_timestamp(self):

        time = 1234345
        with self.assertRaises(SystemExit):
            DatetimeParser.parse_atmotube_timestamp(time)

        time = ""
        with self.assertRaises(SystemExit):
            DatetimeParser.parse_atmotube_timestamp(time)

    def test_last_date_from_api_param(self):
        test_param = {"date": "2021-10-11 09:44:00"}
        expected_date = "2021-10-11"
        expected_time = "09:44:00"
        date, time = DatetimeParser.last_date_from_api_param(test_param)
        self.assertEqual(date, expected_date)
        self.assertEqual(time, expected_time)

    def test_system_exit_when_missing_date_param(self):
        test_param = {}

        with self.assertRaises(SystemExit):
            DatetimeParser.last_date_from_api_param(test_param)


    def test_empty_string_when_date_is_none(self):
        test_param = {"date": None}
        date, time = DatetimeParser.last_date_from_api_param(test_param)
        self.assertEqual(date, "")


    def test_last_timestamp_from_packets(self):
        test_packet = [{f"{TIMESTAMP}": "ts1"}, {f"{TIMESTAMP}": "ts2"}, {f"{TIMESTAMP}": "ts3"}]
        expected_output = "ts3"
        actual_output = DatetimeParser.last_timestamp_from_packets(test_packet)
        self.assertEqual(actual_output, expected_output)



if __name__ == '__main__':
    unittest.main()
