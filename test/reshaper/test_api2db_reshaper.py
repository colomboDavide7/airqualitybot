#################################################
#
# @Author: davidecolombo
# @Date: mar, 26-10-2021, 12:09
# @Description: ENTER DESCRIPTION HERE ...
#
#################################################

import unittest
from airquality.reshaper.api2db_reshaper import API2DatabaseReshaperFactory
from airquality.constants.shared_constants import ATMOTUBE_COORDS_PARAM, ATMOTUBE_TIME_PARAM, \
    RESHAPER2SQLBUILDER_PARAM_ID, RESHAPER2SQLBUILDER_PARAM_VAL, RESHAPER2SQLBUILDER_TIMESTAMP, RESHAPER2SQLBUILDER_GEOMETRY


class TestAPI2DatabaseReshaper(unittest.TestCase):

    def setUp(self) -> None:
        self.factory = API2DatabaseReshaperFactory()

    def test_successfully_reshape_atmotube_packets(self):
        test_packets = [{"par1": "val1", "par2": "val2", ATMOTUBE_TIME_PARAM: "2021-10-11T09:44:00.000Z",
                         ATMOTUBE_COORDS_PARAM: {"lat": 45.232098, "lon": 9.7663}}]

        test_code2id_map = {"par1": 8, "par2": 9}
        expected_output = [{RESHAPER2SQLBUILDER_PARAM_ID: 8, RESHAPER2SQLBUILDER_PARAM_VAL: "'val1'",
                            RESHAPER2SQLBUILDER_TIMESTAMP: "'2021-10-11 09:44:00'",
                            RESHAPER2SQLBUILDER_GEOMETRY: "ST_GeomFromText('POINT(9.7663 45.232098)')"},
                           {RESHAPER2SQLBUILDER_PARAM_ID: 9, RESHAPER2SQLBUILDER_PARAM_VAL: "'val2'",
                            RESHAPER2SQLBUILDER_TIMESTAMP: "'2021-10-11 09:44:00'",
                            RESHAPER2SQLBUILDER_GEOMETRY: "ST_GeomFromText('POINT(9.7663 45.232098)')"}]
        reshaper = self.factory.create_api2database_reshaper(bot_personality = "atmotube")
        actual_output = reshaper.reshape_packets(packets = test_packets, reshape_mapping = test_code2id_map)
        self.assertEqual(actual_output, expected_output)


    def test_empty_list_when_empty_packets_atmotube_reshaper(self):
        test_packets = []

        test_code2id_map = {"par1": 8, "par2": 9}
        expected_output = []
        reshaper = self.factory.create_api2database_reshaper(bot_personality = "atmotube")
        actual_output = reshaper.reshape_packets(packets = test_packets, reshape_mapping = test_code2id_map)
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_when_reshape_parameters_are_empty_atmotube_reshaper(self):
        test_packets = [{"par1": "val1", "par2": "val2", ATMOTUBE_TIME_PARAM: "2021-10-11T09:44:00.000Z",
                         ATMOTUBE_COORDS_PARAM: {"lat": 45.232098, "lon": 9.7663}}]

        test_code2id_map = {}
        reshaper = self.factory.create_api2database_reshaper(bot_personality = "atmotube")
        with self.assertRaises(SystemExit):
            reshaper.reshape_packets(packets = test_packets, reshape_mapping = test_code2id_map)


################################ PURPLE AIR RESHAPER ################################


    def test_successfully_reshape_purpleair_packets(self):

        test_packets = [{"name": "n1", "sensor_index": "idx1", "latitude": "45.123", "longitude": "8.673"},
                        {"name": "n2", "sensor_index": "idx2", "latitude": "45.456", "longitude": "8.123"},
                        {"name": "n3", "sensor_index": "idx3", "latitude": "45.789", "longitude": "8.456"}]

        test_reshape_map = {"n1 (idx1)": "9", "n2 (idx2)": "5", "n3 (idx3)": "14"}

        expected_output = [{"9": "ST_GeomFromText('POINT(8.673 45.123)')"},
                           {"5": "ST_GeomFromText('POINT(8.123 45.456)')"},
                           {"14": "ST_GeomFromText('POINT(8.456 45.789)')"}]
        reshaper = API2DatabaseReshaperFactory().create_api2database_reshaper(bot_personality = "purpleair")
        actual_output = reshaper.reshape_packets(packets = test_packets, reshape_mapping = test_reshape_map)
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_when_missing_name_param_purpleair_reshaper(self):

        test_packets = [{ "latitude": "45.123", "longitude": "8.673"},
                        {"latitude": "45.456", "longitude": "8.123"},
                        { "latitude": "45.789", "longitude": "8.456"}]

        test_reshape_map = {"n1 (idx1)": "9", "n2 (idx2)": "5", "n3 (idx3)": "14"}

        reshaper = API2DatabaseReshaperFactory().create_api2database_reshaper(bot_personality = "purpleair")
        with self.assertRaises(SystemExit):
            reshaper.reshape_packets(packets = test_packets, reshape_mapping = test_reshape_map)


    def test_system_exit_when_missing_geolocation_param_purpleair_reshaper(self):
        test_packets = [{"name": "n1", "sensor_index": "idx1"},
                        {"name": "n2", "sensor_index": "idx2"},
                        {"name": "n3", "sensor_index": "idx3"}]

        test_reshape_map = {"n1 (idx1)": "9", "n2 (idx2)": "5", "n3 (idx3)": "14"}

        reshaper = API2DatabaseReshaperFactory().create_api2database_reshaper(bot_personality = "purpleair")
        with self.assertRaises(SystemExit):
            reshaper.reshape_packets(packets = test_packets, reshape_mapping = test_reshape_map)



if __name__ == '__main__':
    unittest.main()
