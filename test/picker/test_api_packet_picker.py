#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 11:49
# @Description: unit test script
#
#################################################


import unittest
from airquality.picker.api_packet_picker import APIPacketPicker


class TestAPIPacketPicker(unittest.TestCase):


    def test_pick_purpleair_sensor_name_from_identifier(self):
        test_packet = {"name": "n1", "sensor_index": "idx1"}
        expected_output = "n1 (idx1)"
        actual_output = APIPacketPicker.pick_sensor_name_from_identifier(packet = test_packet, identifier = "purpleair")
        self.assertEqual(actual_output, expected_output)


    def test_invalid_purpleair_packet_while_picking_sensor_name(self):
        test_packet = {"arg1": "val1", "arg2": "val2"}
        with self.assertRaises(SystemExit):
            APIPacketPicker.pick_sensor_name_from_identifier(packet = test_packet, identifier = "purpleair")



if __name__ == '__main__':
    unittest.main()
