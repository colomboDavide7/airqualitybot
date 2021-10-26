#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 11:00
# @Description: unit test script
#
#################################################

import unittest
from airquality.reshaper.api_packet_reshaper import APIPacketReshaperFactory
from airquality.constants.shared_constants import PURPLEAIR_FIELDS_PARAM, PURPLEAIR_DATA_PARAM


class TestAPIPacketReshaper(unittest.TestCase):

    def setUp(self) -> None:
        self.factory = APIPacketReshaperFactory()


    def test_reshape_purpleair_packets(self):
        purpleair_reshaper = self.factory.create_api_packet_reshaper(bot_personality = "purpleair")
        test_api_answer = {
            PURPLEAIR_FIELDS_PARAM: ["f1", "f2"],
            PURPLEAIR_DATA_PARAM: [
                ["v1", "v2"],
                ["v3", "v4"]
            ]
        }

        expected_answer = [
            {"f1": "v1", "f2": "v2"},
            {"f1": "v3", "f2": "v4"}
        ]
        actual_answer = purpleair_reshaper.reshape_packet(api_answer = test_api_answer)
        self.assertEqual(actual_answer, expected_answer)


    def test_empty_list_value_when_empty_data_reshape_purpleair_packets(self):
        purpleair_reshaper = self.factory.create_api_packet_reshaper(bot_personality = "purpleair")
        test_api_answer = {
            PURPLEAIR_FIELDS_PARAM: ["f1", "f2"],
            PURPLEAIR_DATA_PARAM: []
        }
        expected_answer = []
        actual_answer = purpleair_reshaper.reshape_packet(api_answer = test_api_answer)
        self.assertEqual(actual_answer, expected_answer)


if __name__ == '__main__':
    unittest.main()
