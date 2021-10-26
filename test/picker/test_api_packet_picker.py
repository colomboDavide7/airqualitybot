#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 11:49
# @Description: unit test script
#
#################################################


import unittest
from airquality.picker.api_packet_picker import APIPacketPickerFactory
from airquality.constants.shared_constants import PURPLE_AIR_API_PARAM


class TestAPIPacketPicker(unittest.TestCase):


    def setUp(self) -> None:
        self.factory = APIPacketPickerFactory()


    def test_successfully_pick_purpleair_api_param(self):
        test_packets = [{"primary_id_a": "idA1", "primary_key_a": "keyA1",
                         "primary_id_b": "idB1", "primary_key_b": "keyB1",
                         "secondary_id_a": "idA2", "secondary_key_a": "keyA2",
                         "secondary_id_b": "idB2", "secondary_key_b": "keyB2",
                         "par1": "val1", "par2": "val2", "par3": "val3"}]

        expected_output = [{"primary_id_a": "idA1", "primary_key_a": "keyA1",
                            "primary_id_b": "idB1", "primary_key_b": "keyB1",
                            "secondary_id_a": "idA2", "secondary_key_a": "keyA2",
                            "secondary_id_b": "idB2", "secondary_key_b": "keyB2"}]
        picker = self.factory.create_api_packet_picker(bot_personality = "purpleair")
        actual_output = picker.pick_packet_params(packets = test_packets, param2pick = PURPLE_AIR_API_PARAM)
        self.assertEqual(actual_output, expected_output)


    def test_empty_list_when_passing_empty_packets_purpleair_picker(self):
        test_packets = []
        expected_output = []
        picker = self.factory.create_api_packet_picker(bot_personality = "purpleair")
        actual_output = picker.pick_packet_params(packets = test_packets, param2pick = PURPLE_AIR_API_PARAM)
        self.assertEqual(actual_output, expected_output)


    def test_same_packets_when_passing_empty_param2pick_purpleair_picker(self):
        test_packets = [{"primary_id_a": "idA1", "primary_key_a": "keyA1",
                         "primary_id_b": "idB1", "primary_key_b": "keyB1",
                         "secondary_id_a": "idA2", "secondary_key_a": "keyA2",
                         "secondary_id_b": "idB2", "secondary_key_b": "keyB2",
                         "par1": "val1", "par2": "val2", "par3": "val3"}]

        expected_output = [{"primary_id_a": "idA1", "primary_key_a": "keyA1",
                            "primary_id_b": "idB1", "primary_key_b": "keyB1",
                            "secondary_id_a": "idA2", "secondary_key_a": "keyA2",
                            "secondary_id_b": "idB2", "secondary_key_b": "keyB2",
                            "par1": "val1", "par2": "val2", "par3": "val3"}]
        picker = self.factory.create_api_packet_picker(bot_personality = "purpleair")
        actual_output = picker.pick_packet_params(packets = test_packets, param2pick = [])
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_when_missing_param2pick_purpleair_picker(self):
        test_packets = [{"primary_id_a": "idA1", "primary_key_a": "keyA1",
                         "primary_id_b": "idB1", "primary_key_b": "keyB1",
                         "secondary_id_a": "idA2", "secondary_key_a": "keyA2",
                         "secondary_id_b": "idB2", "secondary_key_b": "keyB2",
                         "par1": "val1", "par2": "val2", "par3": "val3"}]

        picker = self.factory.create_api_packet_picker(bot_personality = "purpleair")
        with self.assertRaises(SystemExit):
            picker.pick_packet_params(packets = test_packets, param2pick = ["bad_param1", "bad_param2"])





if __name__ == '__main__':
    unittest.main()
