#################################################
#
# @Author: davidecolombo
# @Date: mar, 26-10-2021, 12:57
# @Description: unit test script
#
#################################################

import unittest
from airquality.filter.datetime_packet_filter import DatetimePacketFilterFactory
from airquality.constants.shared_constants import ATMOTUBE_TIME_PARAM


class TestDatetimeFilter(unittest.TestCase):


    def test_successfully_filter_atmotube_packets(self):
        """Test the successful scenario of filtering atmotube packets."""

        test_packets = {"data": {"items": [{ATMOTUBE_TIME_PARAM: "2021-10-11T09:44:00.000Z"},
                                           {ATMOTUBE_TIME_PARAM: "2021-10-11T09:45:00.000Z"},
                                           {ATMOTUBE_TIME_PARAM: "2021-10-11T09:46:00.000Z"}]}}

        test_sqltimestamp = "2021-10-11 09:45:00"
        expected_output = [{ATMOTUBE_TIME_PARAM: "2021-10-11T09:46:00.000Z"}]
        filter_ = DatetimePacketFilterFactory().create_datetime_filter(bot_personality = "atmotube")
        actual_output = filter_.filter_packets(packets = test_packets, sqltimestamp = test_sqltimestamp)
        self.assertEqual(actual_output, expected_output)


    def test_same_packets_when_sqltimestamp_is_empty_atmotube_filter(self):
        """Test same items when no 'sqltimestamp' is provided."""

        test_packets = {"data": {"items": [{ATMOTUBE_TIME_PARAM: "2021-10-11T09:44:00.000Z"},
                                           {ATMOTUBE_TIME_PARAM: "2021-10-11T09:45:00.000Z"},
                                           {ATMOTUBE_TIME_PARAM: "2021-10-11T09:46:00.000Z"}]}}

        test_sqltimestamp = ""
        expected_output = [{ATMOTUBE_TIME_PARAM: "2021-10-11T09:44:00.000Z"},
                           {ATMOTUBE_TIME_PARAM: "2021-10-11T09:45:00.000Z"},
                           {ATMOTUBE_TIME_PARAM: "2021-10-11T09:46:00.000Z"}]
        filter_ = DatetimePacketFilterFactory().create_datetime_filter(bot_personality = "atmotube")
        actual_output = filter_.filter_packets(packets = test_packets, sqltimestamp = test_sqltimestamp)
        self.assertEqual(actual_output, expected_output)


    def test_empty_list_when_items_is_empty_atmotube_filter(self):
        """Test empty list return value."""

        test_packets = {"data": {"items": []}}

        test_sqltimestamp = "2021-10-11 09:45:00"
        expected_output = []
        filter_ = DatetimePacketFilterFactory().create_datetime_filter(bot_personality = "atmotube")
        actual_output = filter_.filter_packets(packets = test_packets, sqltimestamp = test_sqltimestamp)
        self.assertEqual(actual_output, expected_output)



if __name__ == '__main__':
    unittest.main()
