#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 15:26
# @Description: unit test script
#
#################################################


import unittest
from airquality.keeper.api_packet_keeper import APIPacketKeeperFactory
from airquality.packet.apiparam_single_packet import APIParamSinglePacketPurpleair


class TestAPIPacketKeeper(unittest.TestCase):

    def test_successfully_keep_packets_purpleair(self):
        test_packets = [APIParamSinglePacketPurpleair({"name": "n1", "sensor_index": "idx1"}),
                        APIParamSinglePacketPurpleair({"name": "n2", "sensor_index": "idx2"})]

        test_identifier = ["n1 (idx1)"]
        expected_output = [APIParamSinglePacketPurpleair({"name": "n1", "sensor_index": "idx1"})]

        keeper = APIPacketKeeperFactory().create_packet_keeper(bot_personality="purpleair")
        actual_output = keeper.keep_packets(packets=test_packets, identifiers=test_identifier)
        self.assertEqual(actual_output, expected_output)

    def test_empty_list_when_empty_packets_purpleair_keeper(self):
        test_packets = []
        test_identifier = ["n2 (idx2)", "n4 (idx4)"]
        expected_output = []
        keeper = APIPacketKeeperFactory().create_packet_keeper(bot_personality="purpleair")
        actual_output = keeper.keep_packets(packets=test_packets, identifiers=test_identifier)
        self.assertEqual(actual_output, expected_output)

    def test_same_packets_when_empty_identifiers_purpleair_keeper(self):
        test_packets = [APIParamSinglePacketPurpleair({"name": "n1", "sensor_index": "idx1"}),
                        APIParamSinglePacketPurpleair({"name": "n2", "sensor_index": "idx2"})]
        test_identifier = []
        expected_output = [APIParamSinglePacketPurpleair({"name": "n1", "sensor_index": "idx1"}),
                           APIParamSinglePacketPurpleair({"name": "n2", "sensor_index": "idx2"})]
        keeper = APIPacketKeeperFactory().create_packet_keeper(bot_personality="purpleair")
        actual_output = keeper.keep_packets(packets=test_packets, identifiers=test_identifier)
        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest.main()
