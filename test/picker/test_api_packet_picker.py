#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 11:49
# @Description: unit test script
#
#################################################


import unittest
from airquality.picker import TIMESTAMP, PARAM_VALUE, PARAM_ID, GEOMETRY
from airquality.picker.api_packet_picker import APIPacketPicker


class TestAPIPacketPicker(unittest.TestCase):


    def test_pick_only_packets_after_timestamp(self):
        test_packets = [{"param1": "value1",
                        "time": "2021-10-11T09:44:00.000Z"
                         },
                        {"param1": "value1",
                         "time": "2021-10-11T09:45:00.000Z"
                         }]

        test_param_id_codes = {"param1": 1}

        expected_answer = [{f"{PARAM_ID}": 1,
                            f"{PARAM_VALUE}": "'value1'",
                            f"{TIMESTAMP}": "'2021-10-11 09:45:00'",
                            f"{GEOMETRY}": "null"}]
        actual_answer = APIPacketPicker.pick_atmotube_api_packets_from_last_timestamp_on(
                parsed_api_answer = test_packets,
                param_id_code = test_param_id_codes,
                last_timestamp = "2021-10-11 09:44:00"
        )
        self.assertEqual(actual_answer, expected_answer)


    def test_system_exit_pick_last_atmotube_timestamp_when_missing_date(self):
        test_api_param = {"param1": "val1",
                          "param2": "val2"}
        with self.assertRaises(SystemExit):
            APIPacketPicker.pick_last_atmotube_measure_timestamp_or_empty_string(test_api_param)


    def test_return_empty_string_when_date_is_None(self):
        test_api_param = {"param1": "val1",
                          "param2": "val2",
                          "date": None}
        expected_output = ""
        actual_output = APIPacketPicker.pick_last_atmotube_measure_timestamp_or_empty_string(test_api_param)
        self.assertEqual(actual_output, expected_output)

    def test_pick_purpleair_sensor_name_from_identifier(self):
        test_packet = {"name": "n1", "sensor_index": "idx1"}
        expected_output = "n1 (idx1)"
        actual_output = APIPacketPicker.pick_sensor_name_from_identifier(packet = test_packet, identifier = "purpleair")
        self.assertEqual(actual_output, expected_output)


    def test_invalid_purpleair_packet_while_picking_sensor_name(self):
        test_packet = {"arg1": "val1", "arg2": "val2"}
        with self.assertRaises(SystemExit):
            APIPacketPicker.pick_sensor_name_from_identifier(packet = test_packet, identifier = "purpleair")


    def test_missing_required_param_pick_purpleair_api_param_from_packet(self):

        test_packet = {"primary_id_a": "idA", "primary_key_a": "keyA"}
        with self.assertRaises(SystemExit):
            APIPacketPicker.pick_api_param_from_packet(packet = test_packet, identifier = "purpleair")

    def test_successfully_pick_purpleair_api_param(self):
        test_packet = {"primary_id_a": "idA", "primary_key_a": "keyA",
                       "primary_id_b": "idB", "primary_key_b": "keyB",
                       "secondary_id_a": "idA2", "secondary_key_a": "keyA2",
                       "secondary_id_b": "idB2", "secondary_key_b": "keyB2",
                       "ignored": "val", "ignored2": "val2", "ignored3": "val3"}

        expected_output = {"primary_id_a": "idA", "primary_key_a": "keyA",
                           "primary_id_b": "idB", "primary_key_b": "keyB",
                           "secondary_id_a": "idA2", "secondary_key_a": "keyA2",
                           "secondary_id_b": "idB2", "secondary_key_b": "keyB2"}

        actual_output = APIPacketPicker.pick_api_param_from_packet(packet = test_packet, identifier = "purpleair")
        self.assertEqual(actual_output, expected_output)



if __name__ == '__main__':
    unittest.main()
