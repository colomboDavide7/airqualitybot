######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 11:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

import unittest
from data.universal_db_adapter import PurpleairUniversalDatabaseAdapter, AtmotubeUniversalDatabaseAdapter, \
    ThingspeakUniversalDatabaseAdapter


class TestUniversalDatabaseAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.purpleair_adapter = PurpleairUniversalDatabaseAdapter()
        self.atmotube_adapter = AtmotubeUniversalDatabaseAdapter()
        self.thingspeak_adapter = ThingspeakUniversalDatabaseAdapter()

    def test_successfully_adapt_purpleair_packets(self):
        test_packet = {'name': 'n1', 'sensor_index': 'idx1', 'latitude': 'lat_val', 'longitude': 'lng_val',
                       'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A', 'primary_key_b': 'key1B',
                       'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                       'secondary_key_b': 'key2B'}

        expected_output = {'name': 'n1 (idx1)',
                           'type': 'PurpleAir/ThingSpeak',
                           'lat': 'lat_val',
                           'lng': 'lng_val',
                           'param_name': ['primary_id_a', 'primary_id_b', 'primary_key_a', 'primary_key_b',
                                          'secondary_id_a', 'secondary_id_b', 'secondary_key_a', 'secondary_key_b'],
                           'param_value': ['id1A', 'id1B', 'key1A', 'key1B', 'id2A', 'id2B', 'key2A', 'key2B']}

        actual_output = self.purpleair_adapter.adapt(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_occur_purpleair_container_adapter(self):
        test_packet = {'name': 'n1', 'sensor_index': 'idx1',
                       'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                       'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.adapt(test_packet)

    ############################## TEST ATMOTUBE UNIVERSAL ADAPTER #############################

    def test_successfully_adapt_atmotube_packet(self):
        # Test when 'coords' are missing
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                       'p': 'val7', 'time': '2021-10-11T01:33:44.000Z'}
        expected_output = {'timestamp': '2021-10-11 01:33:44',
                           'param_name': ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p'],
                           'param_value': ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7']}
        actual_output = self.atmotube_adapter.adapt(test_packet)
        self.assertEqual(actual_output, expected_output)

        # Test when 'coords' are not missing
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                       'p': 'val7', 'time': '2021-10-11T01:33:44.000Z', 'coords': {'lat': 'lat_val', 'lon': 'lon_val'}}
        expected_output = {'lat': 'lat_val', 'lng': 'lon_val', 'timestamp': '2021-10-11 01:33:44',
                           'param_name': ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p'],
                           'param_value': ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7']}
        actual_output = self.atmotube_adapter.adapt(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_none_value_when_field_is_missing(self):
        # Test output when 't', 'h' and 'p' are missing
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 'time': '2021-10-11T01:33:44.000Z'}
        expected_output = {'timestamp': '2021-10-11 01:33:44',
                           'param_name': ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p'],
                           'param_value': ['val1', 'val2', 'val3', 'val4', None, None, None]}
        actual_output = self.atmotube_adapter.adapt(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_param_is_missing(self):
        # Test when 'coords' are not missing
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                       'p': 'val7', 'coords': {}}
        with self.assertRaises(SystemExit):
            self.atmotube_adapter.adapt(test_packet)

    ############################## TEST THINGSPEAK UNIVERSAL ADAPTER #############################

    def test_successfully_adapt_thingspeak_packets(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'name': 'f1', 'value': 'val1'},
                                  {'name': 'f2', 'value': 'val2'}]}

        expected_output = {'timestamp': '2021-10-11 01:33:44',
                           'param_name': ['f1', 'f2'],
                           'param_value': ['val1', 'val2']}
        actual_output = self.thingspeak_adapter.adapt(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_none_value_when_param_is_null(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'name': 'f1', 'value': None},
                                  {'name': 'f2', 'value': 'val2'}]}

        expected_output = {'timestamp': '2021-10-11 01:33:44',
                           'param_name': ['f1', 'f2'],
                           'param_value': [None, 'val2']}
        actual_output = self.thingspeak_adapter.adapt(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raised(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'name': 'f1', 'bad_key': 'val1'},
                                  {'name': 'f2', 'bad_key': 'val2'}]}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.adapt(test_packet)

        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'bad_key': 'f1', 'value': 'val1'},
                                  {'bad_key': 'f2', 'value': 'val2'}]}

        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.adapt(test_packet)

        test_packet = {'created_at': '2021-10-11T01:33:44Z'}

        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.adapt(test_packet)


if __name__ == '__main__':
    unittest.main()
