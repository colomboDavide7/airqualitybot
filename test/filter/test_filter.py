#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 12:35
# @Description: unit test script
#
#################################################

import unittest
from airquality.filter.filter import APIPacketFilterFactory
from airquality.constants.shared_constants import EMPTY_LIST


class TestFilter(unittest.TestCase):


    def setUp(self) -> None:
        """This method is executed every time before a test."""
        self.factory = APIPacketFilterFactory()


    def test_successfully_filter_purpleair_packets(self):
        """This method tests the correct behaviour of the purple air filter class."""

        test_packets = [{"name": "n1", "sensor_index": "idx1"},
                        {"name": "n2", "sensor_index": "idx2"},
                        {"name": "n3", "sensor_index": "idx3"}]

        test_filter_list = ["n1 (idx1)"]
        expected_output = [{"name": "n2", "sensor_index": "idx2"},
                           {"name": "n3", "sensor_index": "idx3"}]
        purpleair_filter = self.factory.create_api_packet_filter(bot_personality = "purpleair")
        actual_output = purpleair_filter.filter_packet(packets = test_packets, filter_list = test_filter_list)
        self.assertEqual(actual_output, expected_output)


    def test_purpleair_filter_with_empty_filter_list(self):
        """This method tests the behaviour of the purpleair filter method with 'filter_list' argument equal to
        'EMPTY_LIST'."""

        test_packets = [{"name": "n1", "sensor_index": "idx1"},
                        {"name": "n2", "sensor_index": "idx2"},
                        {"name": "n3", "sensor_index": "idx3"}]

        test_filter_list = EMPTY_LIST
        expected_output = [{"name": "n1", "sensor_index": "idx1"},
                           {"name": "n2", "sensor_index": "idx2"},
                           {"name": "n3", "sensor_index": "idx3"}]
        purpleair_filter = self.factory.create_api_packet_filter(bot_personality = "purpleair")
        actual_output = purpleair_filter.filter_packet(packets = test_packets, filter_list = test_filter_list)
        self.assertEqual(actual_output, expected_output)


    def test_purpleair_filter_with_empty_packets(self):
        """This method tests the return value of 'EMPTY_LIST' an empty list of packets is passed as argument."""

        test_packets = EMPTY_LIST
        test_filter_list = ["something1", "something2"]
        expected_output = EMPTY_LIST
        purpleair_filter = self.factory.create_api_packet_filter(bot_personality = "purpleair")
        actual_output = purpleair_filter.filter_packet(packets = test_packets, filter_list = test_filter_list)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
