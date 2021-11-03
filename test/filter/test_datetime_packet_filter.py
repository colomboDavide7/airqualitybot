#################################################
#
# @Author: davidecolombo
# @Date: mar, 26-10-2021, 12:57
# @Description: unit test script
#
#################################################

import unittest
from airquality.filter.datetime_packet_filter import DatetimePacketFilterFactory
from airquality.plain.plain_api_packet import PlainAPIPacketAtmotube


class TestDatetimeFilter(unittest.TestCase):

    def test_successfully_filter_atmotube_packets(self):
        """Test the successful scenario of filtering atmotube packets."""

        test_packets = [PlainAPIPacketAtmotube({'time': "2021-10-11T09:44:00.000Z"}),
                        PlainAPIPacketAtmotube({'time': "2021-10-11T09:45:00.000Z"}),
                        PlainAPIPacketAtmotube({'time': "2021-10-11T09:46:00.000Z"})]

        test_sqltimestamp = "2021-10-11 09:45:00"
        expected_output = [PlainAPIPacketAtmotube({'time': "2021-10-11T09:46:00.000Z"})]
        datetime_filter = DatetimePacketFilterFactory().create_datetime_filter(bot_personality="atmotube")
        actual_output = datetime_filter.filter_packets(packets=test_packets, sqltimestamp=test_sqltimestamp)
        self.assertEqual(actual_output, expected_output)

    def test_same_packets_when_sqltimestamp_is_empty_atmotube_filter(self):
        """Test same items when no 'sqltimestamp' is provided."""

        test_packets = [PlainAPIPacketAtmotube({'time': "2021-10-11T09:44:00.000Z"}),
                        PlainAPIPacketAtmotube({'time': "2021-10-11T09:45:00.000Z"}),
                        PlainAPIPacketAtmotube({'time': "2021-10-11T09:46:00.000Z"})]
        expected_output = [PlainAPIPacketAtmotube({'time': "2021-10-11T09:44:00.000Z"}),
                           PlainAPIPacketAtmotube({'time': "2021-10-11T09:45:00.000Z"}),
                           PlainAPIPacketAtmotube({'time': "2021-10-11T09:46:00.000Z"})]
        test_sqltimestamp = ""
        datetime_filter = DatetimePacketFilterFactory().create_datetime_filter(bot_personality="atmotube")
        actual_output = datetime_filter.filter_packets(packets=test_packets, sqltimestamp=test_sqltimestamp)
        self.assertEqual(actual_output, expected_output)

    def test_empty_list_when_empty_list_is_passed(self):
        """Test empty list return value."""

        test_packets = []
        test_sqltimestamp = "2021-10-11 09:45:00"
        expected_output = []
        datetime_filter = DatetimePacketFilterFactory().create_datetime_filter(bot_personality="atmotube")
        actual_output = datetime_filter.filter_packets(packets=test_packets, sqltimestamp=test_sqltimestamp)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
