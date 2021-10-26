#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 11:49
# @Description: unit test script
#
#################################################


import unittest
from airquality.picker.api_packet_picker import APIPacketPicker
from airquality.constants.shared_constants import ATMOTUBE_TIME_PARAM, ATMOTUBE_COORDS_PARAM, \
    PICKER2SQLBUILDER_PARAM_ID, PICKER2SQLBUILDER_PARAM_VAL, PICKER2SQLBUILDER_TIMESTAMP, PICKER2SQLBUILDER_GEOMETRY


class TestAPIPacketPicker(unittest.TestCase):


    def test_system_exit_pick_last_atmotube_timestamp_when_missing_date(self):
        test_api_param = {"param1": "val1",
                          "param2": "val2"}
        with self.assertRaises(SystemExit):
            APIPacketPicker.pick_date_from_api_param_by_identifier(test_api_param, identifier = "atmotube")


    def test_return_empty_string_when_date_is_None(self):
        test_api_param = {"param1": "val1",
                          "param2": "val2",
                          "date": None}
        expected_output = ""
        actual_output = APIPacketPicker.pick_date_from_api_param_by_identifier(test_api_param, identifier = "atmotube")
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


    def test_successfully_pick_atmotube_packet_timestamp(self):
        test_packet = {ATMOTUBE_TIME_PARAM: "2021-10-11T09:44:00.000Z", "par1": "val1", "par2": "val2"}
        expected_output = "2021-10-11 09:44:00"
        actual_output = APIPacketPicker.pick_packet_timestamp_from_identifier(packet = test_packet, identifier = "atmotube")
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_when_missing_time_key_while_picking_packet_timestamp(self):
        test_packet = {"par1": "val1", "par2": "val2"}
        with self.assertRaises(SystemExit):
            APIPacketPicker.pick_packet_timestamp_from_identifier(packet = test_packet, identifier = "atmotube")


    # def test_successfully_reshape_atmotube_packets(self):
    #     test_packets = [{"par1": "val1", "par2": "val2",
    #                      ATMOTUBE_TIME_PARAM: "2021-10-11T09:44:00.000Z",
    #                      ATMOTUBE_COORDS_PARAM: {"lat": 45.232098, "lon": 9.7663}}]
    #     test_code2id_map = {"par1": 8, "par2": 9}
    #     expected_output = [{PICKER2SQLBUILDER_PARAM_ID: 8, PICKER2SQLBUILDER_PARAM_VAL: "'val1'",
    #                         PICKER2SQLBUILDER_TIMESTAMP: "'2021-10-11 09:44:00'",
    #                         PICKER2SQLBUILDER_GEOMETRY: "ST_GeomFromText('POINT(9.7663 45.232098)')"},
    #                        {PICKER2SQLBUILDER_PARAM_ID: 9, PICKER2SQLBUILDER_PARAM_VAL: "'val2'",
    #                         PICKER2SQLBUILDER_TIMESTAMP: "'2021-10-11 09:44:00'",
    #                         PICKER2SQLBUILDER_GEOMETRY: "ST_GeomFromText('POINT(9.7663 45.232098)')"}]
    #     actual_output = APIPacketPicker.reshape_atmotube_packets(packets = test_packets, paramcode2paramid_map = test_code2id_map)
    #     self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
