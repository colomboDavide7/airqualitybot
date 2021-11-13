######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 13/11/21 15:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import adapter as par


class TestParamReshaper(unittest.TestCase):

    def test_param_reshaper_class(self):
        obj_cls = par.get_param_reshaper_class('atmotube')
        self.assertEqual(obj_cls, par.AtmotubeParamReshaper)

        obj_cls = par.get_param_reshaper_class('thingspeak')
        self.assertEqual(obj_cls, par.ThingspeakParamReshaper)

        with self.assertRaises(SystemExit):
            par.get_param_reshaper_class('purpleair')

    def test_successfully_uniform_reshape_atmotube_api_param(self):
        test_api_param = {'mac': 'some_mac', 'api_key': 'some_key'}
        expected_output = [{'mac': 'some_mac', 'api_key': 'some_key', 'channel_name': 'Main'}]
        actual_output = par.AtmotubeParamReshaper(test_api_param).reshape()
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raised_atmotube_reshaper(self):
        test_api_param_missing_key = {'mac': 'some_mac'}
        with self.assertRaises(SystemExit):
            par.AtmotubeParamReshaper(test_api_param_missing_key).reshape()

        test_api_param_missing_mac = {'api_key': 'some_key'}
        with self.assertRaises(SystemExit):
            par.AtmotubeParamReshaper(test_api_param_missing_mac).reshape()

    ################################ TEST THINGSPEAK PARAM RESHAPER ################################
    def test_successfully_uniform_reshape_thingspeak_api_param(self):
        test_api_param = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B',
                          'primary_key_b': 'key1B',
                          'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B',
                          'secondary_key_b': 'key2B'}
        expected_output = [{'channel_id': 'id1A', 'api_key': 'key1A', 'channel_name': '1A'},
                           {'channel_id': 'id1B', 'api_key': 'key1B', 'channel_name': '1B'},
                           {'channel_id': 'id2A', 'api_key': 'key2A', 'channel_name': '2A'},
                           {'channel_id': 'id2B', 'api_key': 'key2B', 'channel_name': '2B'}]
        actual_output = par.ThingspeakParamReshaper(test_api_param).reshape()
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raised_thingspeak_reshaper(self):
        test_api_param_missing_1a = {'primary_id_b': 'id1B', 'primary_key_b': 'key1B',
                                     'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B',
                                     'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            par.ThingspeakParamReshaper(test_api_param_missing_1a).reshape()

        test_api_param_missing_1b = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A',
                                     'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B',
                                     'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            par.ThingspeakParamReshaper(test_api_param_missing_1b).reshape()

        test_api_param_missing_2a = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B',
                                     'primary_key_b': 'key1B', 'secondary_id_b': 'id2B', 'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            par.ThingspeakParamReshaper(test_api_param_missing_2a).reshape()

        test_api_param_missing_2b = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B',
                                     'primary_key_b': 'key1B', 'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A'}
        with self.assertRaises(SystemExit):
            par.ThingspeakParamReshaper(test_api_param_missing_2b).reshape()


if __name__ == '__main__':
    unittest.main()
