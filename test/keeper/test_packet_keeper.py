#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 15:26
# @Description: unit test script
#
#################################################


import unittest
from airquality.keeper.packets_keeper import APIPacketKeeperFactory


class TestAPIPacketKeeper(unittest.TestCase):


    def test_successfully_keep_packets_purpleair(self):
        test_packets = [{"name": "n1", "sensor_index": "idx1"},
                        {"name": "n2", "sensor_index": "idx2"},
                        {"name": "n3", "sensor_index": "idx3"},
                        {"name": "n4", "sensor_index": "idx4"}]
        test_identifier = ["n2 (idx2)", "n4 (idx4)"]
        expected_output = [{"name": "n2", "sensor_index": "idx2"},
                           {"name": "n4", "sensor_index": "idx4"}]
        keeper = APIPacketKeeperFactory().create_packet_keeper(bot_personality = "purpleair")
        actual_output = keeper.keep_packets(packets = test_packets, identifiers = test_identifier)
        self.assertEqual(actual_output, expected_output)


    def test_empty_list_when_empty_packets_purpleair_keeper(self):
        test_packets = []
        test_identifier = ["n2 (idx2)", "n4 (idx4)"]
        expected_output = []
        keeper = APIPacketKeeperFactory().create_packet_keeper(bot_personality = "purpleair")
        actual_output = keeper.keep_packets(packets = test_packets, identifiers = test_identifier)
        self.assertEqual(actual_output, expected_output)


    def test_same_packets_when_empty_identifiers_purpleair_keeper(self):
        test_packets = [{"name": "n1", "sensor_index": "idx1"},
                        {"name": "n2", "sensor_index": "idx2"},
                        {"name": "n3", "sensor_index": "idx3"},
                        {"name": "n4", "sensor_index": "idx4"}]
        test_identifier = []
        expected_output = [{"name": "n1", "sensor_index": "idx1"},
                           {"name": "n2", "sensor_index": "idx2"},
                           {"name": "n3", "sensor_index": "idx3"},
                           {"name": "n4", "sensor_index": "idx4"}]
        keeper = APIPacketKeeperFactory().create_packet_keeper(bot_personality = "purpleair")
        actual_output = keeper.keep_packets(packets = test_packets, identifiers = test_identifier)
        self.assertEqual(actual_output, expected_output)



if __name__ == "__main__":
    unittest.main()
