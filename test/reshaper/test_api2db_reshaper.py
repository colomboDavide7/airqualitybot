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
    PICKER2SQLBUILDER_PARAM_ID, PICKER2SQLBUILDER_PARAM_VAL, PICKER2SQLBUILDER_TIMESTAMP, PICKER2SQLBUILDER_GEOMETRY

class TestAPI2DatabaseReshaper(unittest.TestCase):


    def setUp(self) -> None:
        self.factory = API2DatabaseReshaperFactory()


    def test_successfully_reshape_atmotube_packets(self):
        test_packets = [{"par1": "val1", "par2": "val2",
                         ATMOTUBE_TIME_PARAM: "2021-10-11T09:44:00.000Z",
                         ATMOTUBE_COORDS_PARAM: {"lat": 45.232098, "lon": 9.7663}}]
        test_code2id_map = {"par1": 8, "par2": 9}
        expected_output = [{PICKER2SQLBUILDER_PARAM_ID: 8, PICKER2SQLBUILDER_PARAM_VAL: "'val1'",
                            PICKER2SQLBUILDER_TIMESTAMP: "'2021-10-11 09:44:00'",
                            PICKER2SQLBUILDER_GEOMETRY: "ST_GeomFromText('POINT(9.7663 45.232098)')"},
                           {PICKER2SQLBUILDER_PARAM_ID: 9, PICKER2SQLBUILDER_PARAM_VAL: "'val2'",
                            PICKER2SQLBUILDER_TIMESTAMP: "'2021-10-11 09:44:00'",
                            PICKER2SQLBUILDER_GEOMETRY: "ST_GeomFromText('POINT(9.7663 45.232098)')"}]
        reshaper = self.factory.create_api2database_reshaper(bot_personality = "atmotube")
        actual_output = reshaper.reshape_packets(packets = test_packets, measure_param_map = test_code2id_map)
        self.assertEqual(actual_output, expected_output)




if __name__ == '__main__':
    unittest.main()
