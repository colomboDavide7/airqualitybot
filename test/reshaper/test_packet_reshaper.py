#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 11:00
# @Description: unit test script
#
#################################################

import unittest
from data.packet_reshaper import PurpleairPacketReshaper, AtmotubePacketReshaper, \
    ThingspeakPacketReshaper


class TestAPIPacketReshaper(unittest.TestCase):

    def test_reshape_purpleair_packets(self):
        purpleair_reshaper = PurpleairPacketReshaper()
        test_api_answer = {
            'fields': ["name", "sensor_index"],
            'data': [
                ["n1", "idx1"],
                ["n2", "idx2"]
            ]
        }

        expected_answer = [{"name": "n1", "sensor_index": "idx1"}, {"name": "n2", "sensor_index": "idx2"}]
        actual_answer = purpleair_reshaper.reshape_packet(api_answer=test_api_answer)
        self.assertEqual(actual_answer, expected_answer)

    def test_empty_list_value_when_empty_data_reshape_purpleair_packets(self):
        purpleair_reshaper = PurpleairPacketReshaper()
        test_api_answer = {
            'fields': ["f1", "f2"],
            'data': []
        }
        expected_answer = []
        actual_answer = purpleair_reshaper.reshape_packet(api_answer=test_api_answer)
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
            {"created_at": "2021-10-27T05:36:59Z",
             'fields': [{'name': 'pm1.0_atm_a', 'value': '42.35'},
                        {'name': 'pm2.5_atm_a', 'value': '63.05'},
                        {'name': 'pm10.0_atm_a', 'value': '76.32'},
                        {'name': 'temperature_a', 'value': '50'},
                        {'name': 'humidity_a', 'value': '60'}],
             },
            {"created_at": "2021-10-27T05:38:59Z",
             'fields': [{'name': 'pm1.0_atm_a', 'value': '41.07'},
                        {'name': 'pm2.5_atm_a', 'value': '61.54'},
                        {'name': 'pm10.0_atm_a', 'value': '70.31'},
                        {'name': 'temperature_a', 'value': '50'},
                        {'name': 'humidity_a', 'value': '60'}],
             }]

        thingspeak_reshaper = ThingspeakPacketReshaper()
        actual_output = thingspeak_reshaper.reshape_packet(api_answer=test_api_answer)
        self.assertEqual(actual_output, expected_answer)

    def test_system_exit_when_fields_to_use_is_none(self):
        test_api_answer = {"channel": {"name": "BAD NAME",                  # THIS IS WHAT WE WANT TO TEST HERE !!!
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
        thingspeak_reshaper = ThingspeakPacketReshaper()
        with self.assertRaises(SystemExit):
            thingspeak_reshaper.reshape_packet(test_api_answer)

    def test_empty_packets_when_feeds_is_empty(self):
        test_api_answer = {"channel": {'param1': 'val1'},
                           "feeds": []}
        expected_answer = []
        thingspeak_reshaper = ThingspeakPacketReshaper()
        actual_output = thingspeak_reshaper.reshape_packet(api_answer=test_api_answer)
        self.assertEqual(actual_output, expected_answer)

    ################################ TEST RESHAPE ATMOTUBE API PACKET ################################

    def test_successfully_reshaper_atmotube_packets(self):
        test_api_answer = {"data": {"items":
                                    [{'time': "2021-10-02T00:00:00.000Z"},
                                     {'time': "2021-10-02T00:01:00.000Z"}]
                                    }
                           }

        expected_output = [{'time': "2021-10-02T00:00:00.000Z"}, {'time': "2021-10-02T00:01:00.000Z"}]
        atmotube_reshaper = AtmotubePacketReshaper()
        actual_output = atmotube_reshaper.reshape_packet(api_answer=test_api_answer)
        self.assertEqual(actual_output, expected_output)

    def test_empty_list_when_items_is_empty(self):
        test_api_answer = {"data": {"items": []}}

        expected_output = []
        atmotube_reshaper = AtmotubePacketReshaper()
        actual_output = atmotube_reshaper.reshape_packet(api_answer=test_api_answer)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()

    # test_api_answer = {"channel": {"name": "AirMonitor_4e17",
    #                                "field1": "PM1.0 (ATM)",
    #                                "field2": "PM2.5 (ATM)",
    #                                "field3": "PM10.0 (ATM)",
    #                                "field4": "Uptime",
    #                                "field5": "RSSI",
    #                                "field6": "Temperature",
    #                                "field7": "Humidity",
    #                                "field8": "PM2.5 (CF=1)",
    #                                "created_at": "2018-07-12T21:59:03Z",
    #                                "p1": "v1", "p2": "v2"
    #                                },
    #                    "feeds": [
    #                        {"created_at": "2021-10-27T05:36:59Z",
    #                         "entry_id": 910021,
    #                         "field1": "42.35",
    #                         "field2": "63.05",
    #                         "field3": "76.32",
    #                         "field4": "6022",
    #                         "field5": "-60",
    #                         "field6": "50",
    #                         "field7": "60",
    #                         "field8": "53.63"},
    #                        {"created_at": "2021-10-27T05:38:59Z",
    #                         "entry_id": 910022,
    #                         "field1": "41.07",
    #                         "field2": "61.54",
    #                         "field3": "70.31",
    #                         "field4": "6024",
    #                         "field5": "-61",
    #                         "field6": "50",
    #                         "field7": "60",
    #                         "field8": "52.85"}
    #                    ]}
    #
    # expected_answer = [
    #     {"created_at": "2021-10-27 05:36:59",
    #      "pm1.0_atm_a": '42.35',
    #      "pm2.5_atm_a": '63.05',
    #      "pm10.0_atm_a": '76.32',
    #      "temperature_a": '50',
    #      "humidity_a": '60'},
    #     {"created_at": "2021-10-27 05:38:59",
    #      "pm1.0_atm_a": '41.07',
    #      "pm2.5_atm_a": '61.54',
    #      "pm10.0_atm_a": '70.31',
    #      "temperature_a": '50',
    #      "humidity_a": '60'}]
