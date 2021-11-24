######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 13/11/21 15:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.to_delete.db2api.param as par
import airquality.to_delete.config as adapt_const


class TestParamAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_adapter = par.AtmotubeParamAdapter()
        self.thingspeak_adapter = par.ThingspeakParamAdapter()

    def test_param_reshaper_class(self):
        obj_cls = par.get_param_adapter('atmotube')
        self.assertEqual(obj_cls.__class__, par.AtmotubeParamAdapter)

        obj_cls = par.get_param_adapter('thingspeak')
        self.assertEqual(obj_cls.__class__, par.ThingspeakParamAdapter)

        with self.assertRaises(SystemExit):
            par.get_param_adapter('purpleair')

    def test_successfully_reshape_atmotube_api_param(self):
        test_api_param = {adapt_const.MAC_ADDR: 'some_mac',
                          adapt_const.API_KEY: 'some_key'}
        expected_output = [{adapt_const.MAC_ADDR: 'some_mac',
                            adapt_const.API_KEY: 'some_key',
                            adapt_const.CH_NAME: adapt_const.ATMOTUBE_CHANNEL}]
        actual_output = self.atmotube_adapter.reshape(test_api_param)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_atmotube_api_key(self):
        test_api_param_missing_key = {adapt_const.MAC_ADDR: 'some_mac'}
        with self.assertRaises(SystemExit):
            self.atmotube_adapter.reshape(test_api_param_missing_key)

    def test_exit_on_missing_atmotube_mac_address(self):
        test_api_param_missing_mac = {adapt_const.API_KEY: 'some_key'}
        with self.assertRaises(SystemExit):
            self.atmotube_adapter.reshape(test_api_param_missing_mac)

    ################################ TEST THINGSPEAK PARAM RESHAPER ################################
    def test_successfully_uniform_reshape_thingspeak_api_param(self):
        test_api_param = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B', 'primary_key_b': 'key1B',
                          'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B', 'secondary_key_b': 'key2B'}
        expected_output = [{adapt_const.CH_ID: 'id1A', adapt_const.API_KEY: 'key1A', adapt_const.CH_NAME: adapt_const.FST_CH_A},
                           {adapt_const.CH_ID: 'id1B', adapt_const.API_KEY: 'key1B', adapt_const.CH_NAME: adapt_const.FST_CH_B},
                           {adapt_const.CH_ID: 'id2A', adapt_const.API_KEY: 'key2A', adapt_const.CH_NAME: adapt_const.SND_CH_A},
                           {adapt_const.CH_ID: 'id2B', adapt_const.API_KEY: 'key2B', adapt_const.CH_NAME: adapt_const.SND_CH_B}]
        actual_output = self.thingspeak_adapter.reshape(test_api_param)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_thingspeak_channel_a_primary_data(self):
        test_api_param_missing_1a = {'primary_id_b': 'id1B', 'primary_key_b': 'key1B',
                                     'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B',
                                     'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_api_param_missing_1a)

    def test_exit_on_missing_thingspeak_channel_b_primary_data(self):
        test_api_param_missing_1b = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A',
                                     'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B',
                                     'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_api_param_missing_1b)

    def test_exit_on_missing_thingspeak_channel_a_secondary_data(self):
        test_api_param_missing_2a = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B',
                                     'primary_key_b': 'key1B', 'secondary_id_b': 'id2B', 'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_api_param_missing_2a)

    def test_exit_on_missing_thingspeak_channel_b_secondary_data(self):
        test_api_param_missing_2b = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B',
                                     'primary_key_b': 'key1B', 'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A'}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_api_param_missing_2b)


if __name__ == '__main__':
    unittest.main()
