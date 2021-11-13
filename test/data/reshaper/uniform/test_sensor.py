######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 13/11/21 15:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import adapter as sens


class TestSensorReshaper(unittest.TestCase):

    def test_get_sensor_reshaper_class(self):
        obj_cls = sens.get_sensor_reshaper_class('purpleair')
        self.assertEqual(obj_cls, sens.PurpleairSensorReshaper)

        with self.assertRaises(SystemExit):
            sens.get_sensor_reshaper_class('bad sensor type')

    def test_successfully_reshape_purpleair_sensor_data(self):
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

        actual_output = sens.PurpleairSensorReshaper(test_packet).reshape()
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_on_key_error_purpleair(self):
        test_packet = {'name': 'n1', 'sensor_index': 'idx1',
                       'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                       'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A'}
        with self.assertRaises(SystemExit):
            sens.PurpleairSensorReshaper(test_packet).reshape()


if __name__ == '__main__':
    unittest.main()
