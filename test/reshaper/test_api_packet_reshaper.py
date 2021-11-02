#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 11:00
# @Description: unit test script
#
#################################################

import unittest
from airquality.reshaper.api_packet_reshaper import APIPacketReshaperFactory
from airquality.packet.plain_api_packet import PlainAPIPacketPurpleair
from airquality.constants.shared_constants import PURPLEAIR_FIELDS_PARAM, PURPLEAIR_DATA_PARAM


class TestAPIPacketReshaper(unittest.TestCase):

    def setUp(self) -> None:
        self.factory = APIPacketReshaperFactory()

    def test_reshape_purpleair_packets(self):
        purpleair_reshaper = self.factory.create_api_packet_reshaper(bot_personality = "purpleair")
        test_api_answer = {
            PURPLEAIR_FIELDS_PARAM: ["name", "sensor_index"],
            PURPLEAIR_DATA_PARAM: [
                ["n1", "idx1"],
                ["n2", "idx2"]
            ]
        }

        expected_answer = [
            PlainAPIPacketPurpleair({"name": "n1", "sensor_index": "idx1"}),
            PlainAPIPacketPurpleair({"name": "n2", "sensor_index": "idx2"})
        ]
        actual_answer = purpleair_reshaper.reshape_packet(api_answer = test_api_answer)
        self.assertEqual(actual_answer, expected_answer)

    def test_empty_list_value_when_empty_data_reshape_purpleair_packets(self):
        purpleair_reshaper = self.factory.create_api_packet_reshaper(bot_personality = "purpleair")
        test_api_answer = {
            PURPLEAIR_FIELDS_PARAM: ["f1", "f2"],
            PURPLEAIR_DATA_PARAM: []
        }
        expected_answer = []
        actual_answer = purpleair_reshaper.reshape_packet(api_answer = test_api_answer)
        self.assertEqual(actual_answer, expected_answer)

    ################################ TEST RESHAPE THINGSPEAK API PACKET ################################

    def test_successfully_reshape_thingspeak_api_packets(self):
        test_api_answer = {"channel": {"name": "AirMonitor_4e17",
                                       "field1": "PM1.0 (ATM)",
                                       "field2": "PM2.5 (ATM)",
                                       "field3": "PM10.0 (ATM)",
                                       "field4": "Uptime",
                                       "field5": "RSSI",
                                       "field6": "Temperature",
                                       "field7": "Humidity",
                                       "field8": "PM2.5 (CF=1)",
                                       "created_at": "2018-07-12T21:59:03Z",
                                       "p1": "v1", "p2": "v2"
                                       },
                           "feeds": [
                               {"created_at": "2021-10-27T05:36:59Z",
                                "entry_id": 910021,
                                "field1": "42.35",
                                "field2": "63.05",
                                "field3": "76.32",
                                "field4": "6022",
                                "field5": "-60",
                                "field6": "50",
                                "field7": "60",
                                "field8": "53.63"},
                               {"created_at": "2021-10-27T05:38:59Z",
                                "entry_id": 910022,
                                "field1": "41.07",
                                "field2": "61.54",
                                "field3": "70.31",
                                "field4": "6024",
                                "field5": "-61",
                                "field6": "50",
                                "field7": "60",
                                "field8": "52.85"}
                           ]}

        expected_answer = [
            {"time": "2021-10-27 05:36:59",
             "pm1.0_atm_a": '42.35',
             "pm2.5_atm_a": '63.05',
             "pm10.0_atm_a": '76.32',
             "temperature_a": '50',
             "humidity_a": '60'},
            {"time": "2021-10-27 05:38:59",
             "pm1.0_atm_a": '41.07',
             "pm2.5_atm_a": '61.54',
             "pm10.0_atm_a": '70.31',
             "temperature_a": '50',
             "humidity_a": '60'}]

        reshaper = APIPacketReshaperFactory().create_api_packet_reshaper(bot_personality = "thingspeak")
        actual_output = reshaper.reshape_packet(api_answer = test_api_answer)
        self.assertEqual(actual_output, expected_answer)


if __name__ == '__main__':
    unittest.main()
