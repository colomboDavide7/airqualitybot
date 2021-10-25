#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 11:00
# @Description: unit test script
#
#################################################

import unittest
from airquality.reshaper.reshaper import APIPacketReshaperFactory, APIPacketReshaper


class TestAPIPacketReshaper(unittest.TestCase):

    def setUp(self) -> None:
        self.factory = APIPacketReshaperFactory()


    def test_reshaper_factory(self):
        reshaper = self.factory.create_api_packet_reshaper(bot_personality = "purpleair")
        self.assertIsInstance(reshaper, APIPacketReshaper)
        self.assertIsNotNone(reshaper)


    def test_system_exit_with_invalid_personality(self):
        with self.assertRaises(SystemExit):
            self.factory.create_api_packet_reshaper(bot_personality = "bad_bot_personality")


    def test_reshape_purpleair_packets(self):
        purpleair_reshaper = self.factory.create_api_packet_reshaper(bot_personality = "purpleair")
        test_api_answer = {
            "fields": ["f1", "f2"],
            "data": [
                ["v1", "v2"],
                ["v3", "v4"]
            ]
        }

        expected_answer = [
            {"f1": "v1", "f2": "v2"},
            {"f1": "v3", "f2": "v4"}
        ]
        actual_answer = purpleair_reshaper.reshape_packet(parsed_api_answer = test_api_answer)
        self.assertEqual(actual_answer, expected_answer)



if __name__ == '__main__':
    unittest.main()
