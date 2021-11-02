#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 15:25
# @Description: unit test script
#
#################################################


import unittest
from airquality.reshaper.db2api_reshaper import Database2APIReshaperFactory


class TestDatabase2APIReshaper(unittest.TestCase):

    def test_successfully_reshape_thingspeak_api_param(self):
        test_param = {"primary_id_a": "idA1", "primary_id_b": "idB1", "secondary_id_a": "idA2", "secondary_id_b": "idB2",
                      "primary_key_a": "kA1", "primary_key_b": "kB1", "secondary_key_a": "kA2", "secondary_key_b": "kB2",
                      "primary_timestamp_a": "ts1a", "primary_timestamp_b": "ts1b", "secondary_timestamp_a": "ts2a",
                      "secondary_timestamp_b": "ts2b"}

        expected_output = {"idA1": {"key": "kA1", "ts": "ts1a", "name": "primary_timestamp_a"},
                           "idB1": {"key": "kB1", "ts": "ts1b", "name": "primary_timestamp_b"},
                           "idA2": {"key": "kA2", "ts": "ts2a", "name": "secondary_timestamp_a"},
                           "idB2": {"key": "kB2", "ts": "ts2b", "name": "secondary_timestamp_b"}}

        reshaper = Database2APIReshaperFactory().create_reshaper(bot_personality="thingspeak")
        actual_output = reshaper.reshape_data(api_param=test_param)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_api_param_is_empty(self):
        test_param = {}
        reshaper = Database2APIReshaperFactory().create_reshaper(bot_personality="thingspeak")
        with self.assertRaises(SystemExit):
            reshaper.reshape_data(api_param=test_param)

    def test_system_exit_when_missing_keys_from_api(self):
        test_param = {"primary_id_b": "idB1", "secondary_id_a": "idA2", "secondary_id_b": "idB2",
                      "primary_key_a": "kA1", "primary_key_b": "kB1", "secondary_key_a": "kA2"}

        reshaper = Database2APIReshaperFactory().create_reshaper(bot_personality="thingspeak")
        with self.assertRaises(SystemExit):
            reshaper.reshape_data(api_param=test_param)


if __name__ == '__main__':
    unittest.main()
