######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 09/11/21 11:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.data.reshaper.uniform.db2api as rshp


class TestUniversalAPIAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_reshaper = rshp.AtmotubeUniformReshaper()
        self.thingspeak_reshaper = rshp.ThingspeakUniformReshaper()

    def test_successfully_uniform_reshape_atmotube_api_param(self):
        test_api_param = {'mac': 'some_mac', 'api_key': 'some_key'}
        expected_output = [{'mac': 'some_mac', 'api_key': 'some_key'}]
        actual_output = self.atmotube_reshaper.db2api(test_api_param)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raised_atmotube_reshaper(self):
        test_api_param_missing_key = {'mac': 'some_mac'}
        with self.assertRaises(SystemExit):
            self.atmotube_reshaper.db2api(test_api_param_missing_key)

        test_api_param_missing_mac = {'api_key': 'some_key'}
        with self.assertRaises(SystemExit):
            self.atmotube_reshaper.db2api(test_api_param_missing_mac)

    ################################ TEST THINGSPEAK UNIVERSAL ADAPTER ################################
    def test_successfully_uniform_reshape_thingspeak_api_param(self):
        test_api_param = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B',
                          'primary_key_b': 'key1B',
                          'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B',
                          'secondary_key_b': 'key2B'}
        expected_output = [{'channel_id': 'id1A', 'api_key': 'key1A'}, {'channel_id': 'id1B', 'api_key': 'key1B'},
                           {'channel_id': 'id2A', 'api_key': 'key2A'}, {'channel_id': 'id2B', 'api_key': 'key2B'}]
        actual_output = self.thingspeak_reshaper.db2api(test_api_param)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raised_thingspeak_reshaper(self):
        test_api_param_missing_1a = {'primary_id_b': 'id1B', 'primary_key_b': 'key1B',
                                     'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B',
                                     'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.thingspeak_reshaper.db2api(test_api_param_missing_1a)

        test_api_param_missing_1b = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A',
                                     'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B',
                                     'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.thingspeak_reshaper.db2api(test_api_param_missing_1b)

        test_api_param_missing_2a = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B',
                                     'primary_key_b': 'key1B', 'secondary_id_b': 'id2B', 'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.thingspeak_reshaper.db2api(test_api_param_missing_2a)

        test_api_param_missing_2b = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B',
                                     'primary_key_b': 'key1B', 'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A'}
        with self.assertRaises(SystemExit):
            self.thingspeak_reshaper.db2api(test_api_param_missing_2b)


if __name__ == '__main__':
    unittest.main()
