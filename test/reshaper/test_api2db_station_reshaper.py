#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 21:00
# @Description: unit test script
#
#################################################

import unittest
from airquality.reshaper.api2db_station_reshaper import API2DatabaseStationReshaperFactory
from airquality.api2database.measurement_packet import StationMeasurementPacket


class TestAPI2DatabaseStationReshaper(unittest.TestCase):

    def test_successfully_reshape_thingspeak_packets(self):
        test_api_answer = [{"par1": "val1", "par2": "val2", "time": "ts1"},
                           {"par1": "val3", "par2": "val4", "time": "ts2"}]

        test_mapping = {"par1": 1, "par2": 2}

        expected_output = [StationMeasurementPacket(param_id=1, param_val="val1", timestamp="ts1", sensor_id=1),
                           StationMeasurementPacket(param_id=2, param_val="val2", timestamp="ts1", sensor_id=1),
                           StationMeasurementPacket(param_id=1, param_val="val3", timestamp="ts2", sensor_id=1),
                           StationMeasurementPacket(param_id=2, param_val="val4", timestamp="ts2", sensor_id=1)]

        reshaper = API2DatabaseStationReshaperFactory().create_reshaper(bot_personality="thingspeak")
        actual_output = reshaper.reshape_packets(packets=test_api_answer, sensor_id=1, measure_param_map=test_mapping)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_reshaping_with_empty_mapping_thingspeak(self):
        test_api_answer = [{"par1": "val1", "par2": "val2", "time": "ts1"},
                           {"par1": "val3", "par2": "val4", "time": "ts2"}]

        test_mapping = {}

        reshaper = API2DatabaseStationReshaperFactory().create_reshaper(bot_personality="thingspeak")
        with self.assertRaises(SystemExit):
            reshaper.reshape_packets(packets=test_api_answer, sensor_id=1, measure_param_map=test_mapping)

    def test_empty_list_when_empty_packets_is_passed_thingspeak_reshaper(self):
        test_api_answer = []

        test_mapping = {"par1": 1, "par2": 2}

        reshaper = API2DatabaseStationReshaperFactory().create_reshaper(bot_personality="thingspeak")
        actual_output = reshaper.reshape_packets(packets=test_api_answer, sensor_id=1,
                                                 measure_param_map=test_mapping)
        self.assertEqual(actual_output, [])


if __name__ == '__main__':
    unittest.main()
