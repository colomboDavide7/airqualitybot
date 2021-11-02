#################################################
#
# @Author: davidecolombo
# @Date: mar, 26-10-2021, 12:09
# @Description: ENTER DESCRIPTION HERE ...
#
#################################################

import unittest
from airquality.reshaper.dict2mobilepacket_reshaper import Dict2MobilepacketReshaperFactory
from airquality.api2database.measurement_packet import MobileMeasurementPacket
from airquality.constants.shared_constants import ATMOTUBE_COORDS_PARAM, ATMOTUBE_TIME_PARAM


class TestDict2MobilepacketReshaper(unittest.TestCase):

    def setUp(self) -> None:
        self.factory = Dict2MobilepacketReshaperFactory()

    def test_successfully_reshape_atmotube_packets(self):
        test_packets = [{"par1": "val1", "par2": "val2", ATMOTUBE_TIME_PARAM: "2021-10-11T09:44:00.000Z",
                         ATMOTUBE_COORDS_PARAM: {"lat": 45.232098, "lon": 9.7663}}]

        test_code2id_map = {"par1": 8, "par2": 9}
        expected_output = [MobileMeasurementPacket(param_id=8, param_val="val1", timestamp="2021-10-11 09:44:00",
                                                   geom="ST_GeomFromText('POINT(9.7663 45.232098)')"),
                           MobileMeasurementPacket(param_id=9, param_val="val2", timestamp="2021-10-11 09:44:00",
                                                   geom="ST_GeomFromText('POINT(9.7663 45.232098)')")]

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


if __name__ == '__main__':
    unittest.main()
