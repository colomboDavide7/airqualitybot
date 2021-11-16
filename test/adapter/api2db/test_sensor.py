######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 13/11/21 15:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.adapter.api2db.sensor as sens


class TestSensorReshaper(unittest.TestCase):

    def setUp(self) -> None:
        self.purpleair_adapter = sens.get_sensor_adapter('purpleair')

    def test_get_sensor_reshaper_class(self):
        self.assertEqual(self.purpleair_adapter.__class__, sens.PurpleairSensorAdapter)

        with self.assertRaises(SystemExit):
            sens.get_sensor_adapter('bad sensor type')

    def test_successfully_reshape_purpleair_sensor_data(self):
        test_packet = {'name': 'n1', 'sensor_index': 'idx1', 'latitude': 'lat_val', 'longitude': 'lng_val',
                       'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                       'primary_key_b': 'key1B',
                       'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                       'secondary_key_b': 'key2B', 'date_created': 'd'}

        expected_output = {'name': 'n1 (idx1)',
                           'type': 'PurpleAir/ThingSpeak',
                           'lat': 'lat_val',
                           'lng': 'lng_val',
                           'param_name': ['primary_id_a', 'primary_id_b', 'primary_key_a', 'primary_key_b',
                                          'secondary_id_a', 'secondary_id_b', 'secondary_key_a', 'secondary_key_b'],
                           'param_value': ['id1A', 'id1B', 'key1A', 'key1B', 'id2A', 'id2B', 'key2A', 'key2B'],
                           'channel': ['1A', '1B', '2A', '2B'],
                           'last_acquisition': [{'timestamp': 'd'}, {'timestamp': 'd'}, {'timestamp': 'd'}, {'timestamp': 'd'}]}

        actual_output = self.purpleair_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_on_key_error_purpleair(self):
        test_missing_api_param = {'name': 'n1', 'sensor_index': 'idx1',
                                  'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                                  'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.reshape(test_missing_api_param)

        test_missing_name = {'latitude': 'lat_val', 'longitude': 'lng_val',
                             'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                             'primary_key_b': 'key1B',
                             'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                             'secondary_key_b': 'key2B', 'date_created': 'd'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.reshape(test_missing_name)

        test_missing_geom = {'name': 'n1', 'sensor_index': 'idx1',
                             'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                             'primary_key_b': 'key1B',
                             'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                             'secondary_key_b': 'key2B', 'date_created': 'd'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.reshape(test_missing_geom)

        test_missing_date_created = {'name': 'n1', 'sensor_index': 'idx1', 'latitude': 'lat_val',
                                     'longitude': 'lng_val',
                                     'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                                     'primary_key_b': 'key1B',
                                     'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                                     'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.purpleair_adapter.reshape(test_missing_date_created)


if __name__ == '__main__':
    unittest.main()
