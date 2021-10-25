#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 12:35
# @Description: unit test script
#
#################################################

import unittest
from airquality.filter.filter import APIPacketFilterFactory, APIPacketFilter
from airquality.app import EMPTY_LIST



class TestFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.factory = APIPacketFilterFactory()

    def test_make_filter(self):

        filter_ = self.factory.create_api_packet_filter(bot_personality = "purpleair")
        self.assertIsNotNone(filter_)
        self.assertIsInstance(filter_, APIPacketFilter)

    def test_system_exit_bad_personality(self):

        with self.assertRaises(SystemExit):
            self.factory.create_api_packet_filter("bad_bot_personality")

    def test_purpleair_filter(self):

        test_packets = [{"name": "n1"},
                        {"name": "n2"},
                        {"name": "n3"}]

        test_filter_list = ["n1"]
        expected_output = [{"name": "n2"},
                           {"name": "n3"}]
        purpleair_filter = self.factory.create_api_packet_filter(bot_personality = "purpleair")
        actual_output = purpleair_filter.filter_packet(packets = test_packets, filter_list = test_filter_list)
        self.assertEqual(actual_output, expected_output)


    def test_purpleair_filter_with_empty_filter_list(self):
        test_packets = [{"name": "n1"},
                        {"name": "n2"},
                        {"name": "n3"}]

        test_filter_list = []
        expected_output = [{"name": "n1"},
                           {"name": "n2"},
                           {"name": "n3"}]
        purpleair_filter = self.factory.create_api_packet_filter(bot_personality = "purpleair")
        actual_output = purpleair_filter.filter_packet(packets = test_packets, filter_list = test_filter_list)
        self.assertEqual(actual_output, expected_output)


    def test_purpleair_filter_with_empty_packets(self):
        test_packets = EMPTY_LIST
        test_filter_list = ["something1", "something2"]
        expected_output = EMPTY_LIST
        purpleair_filter = self.factory.create_api_packet_filter(bot_personality = "purpleair")
        actual_output = purpleair_filter.filter_packet(packets = test_packets, filter_list = test_filter_list)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
