#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 21:00
# @Description: unit test script
#
#################################################


import unittest
from airquality.reshaper.api2db_station_reshaper import API2DatabaseStationReshaperFactory
from airquality.constants.shared_constants import RESHAPER2SQLBUILDER_TIMESTAMP, RESHAPER2SQLBUILDER_PARAM_VAL, \
    RESHAPER2SQLBUILDER_PARAM_ID, RESHAPER2SQLBUILDER_SENSOR_ID



class TestAPI2DatabaseStationReshaper(unittest.TestCase):


    def test_successfully_reshape_thingspeak_packets(self):

        test_api_answer = [{"par1": "val1", "par2": "val2", "time": "ts1"},
                           {"par1": "val3", "par2": "val4", "time": "ts2"}]

        test_mapping = {"par1": 1, "par2": 2}

        expected_output = [{RESHAPER2SQLBUILDER_PARAM_ID: 1,
                            RESHAPER2SQLBUILDER_SENSOR_ID: 1,
                            RESHAPER2SQLBUILDER_PARAM_VAL: "'val1'",
                            RESHAPER2SQLBUILDER_TIMESTAMP: "'ts1'"},
                           {RESHAPER2SQLBUILDER_PARAM_ID: 2,
                            RESHAPER2SQLBUILDER_SENSOR_ID: 1,
                            RESHAPER2SQLBUILDER_PARAM_VAL: "'val2'",
                            RESHAPER2SQLBUILDER_TIMESTAMP: "'ts1'"},
                           {RESHAPER2SQLBUILDER_PARAM_ID: 1,
                            RESHAPER2SQLBUILDER_SENSOR_ID: 1,
                            RESHAPER2SQLBUILDER_PARAM_VAL: "'val3'",
                            RESHAPER2SQLBUILDER_TIMESTAMP: "'ts2'"},
                           {RESHAPER2SQLBUILDER_PARAM_ID: 2,
                            RESHAPER2SQLBUILDER_SENSOR_ID: 1,
                            RESHAPER2SQLBUILDER_PARAM_VAL: "'val4'",
                            RESHAPER2SQLBUILDER_TIMESTAMP: "'ts2'"},
                           ]


        reshaper = API2DatabaseStationReshaperFactory().create_reshaper(bot_personality = "thingspeak")
        actual_output = reshaper.reshape_packets(packets = test_api_answer, sensor_id = 1, measure_param_map = test_mapping)
        self.assertEqual(actual_output, expected_output)



if __name__ == '__main__':
    unittest.main()
