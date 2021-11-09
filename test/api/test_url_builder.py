#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: unit test script
#
#################################################

import unittest
from airquality.api.url_builder import URLBuilderPurpleair, URLBuilderAtmotube, URLBuilderThingspeak


class TestURLBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.api_address = 'some_api_address'

    def test_successfully_build_purpleair_url(self):
        test_param = {"api_key": "key", "fields": ["f1", "f2"], "opt": "val"}
        expected_output = "some_api_address?api_key=key&fields=f1,f2&opt=val"
        purpleair_builder = URLBuilderPurpleair(api_address=self.api_address, parameters=test_param)
        actual_output = purpleair_builder.build_url()
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_building_purpleair_url(self):
        test_param_missing_key = {"fields": ["f1", "f2"], "opt": "val"}
        purpleair_builder = URLBuilderPurpleair(api_address=self.api_address, parameters=test_param_missing_key)
        with self.assertRaises(SystemExit):
            purpleair_builder.build_url()

        test_param_missing_fields = {"api_key": "some_key", "opt": "val"}
        purpleair_builder = URLBuilderPurpleair(api_address=self.api_address, parameters=test_param_missing_fields)
        with self.assertRaises(SystemExit):
            purpleair_builder.build_url()

        test_param_empty_fields = {"api_key": "some_key", "fields": [], "opt": "val"}
        purpleair_builder = URLBuilderPurpleair(api_address=self.api_address, parameters=test_param_empty_fields)
        with self.assertRaises(SystemExit):
            purpleair_builder.build_url()

    ################################ TEST BUILD ATMOTUBE URL ################################
    def test_successfully_build_atmotube_url(self):
        test_param = {"api_key": "key", 'mac': 'some_mac', "opt": "val"}
        expected_output = "some_api_address?api_key=key&mac=some_mac&opt=val"
        atmotube_builder = URLBuilderAtmotube(api_address=self.api_address, parameters=test_param)
        actual_output = atmotube_builder.build_url()
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_building_atmotube_url(self):
        test_param_missing_key = {'mac': 'some_mac', "opt": "val"}
        atmotube_builder = URLBuilderAtmotube(api_address=self.api_address, parameters=test_param_missing_key)
        with self.assertRaises(SystemExit):
            atmotube_builder.build_url()

        test_param_missing_mac = {"api_key": "key", "opt": "val"}
        atmotube_builder = URLBuilderAtmotube(api_address=self.api_address, parameters=test_param_missing_mac)
        with self.assertRaises(SystemExit):
            atmotube_builder.build_url()

    ################################ TEST BUILD THINGSPEAK URL ################################
    def test_successfully_build_thingspeak_url(self):
        test_param = {"channel_id": "id", 'format': 'json', "api_key": "key", "opt": "val"}
        expected_output = "some_api_address/id/feeds.json?api_key=key&opt=val"
        thingspeak_builder = URLBuilderThingspeak(api_address=self.api_address, parameters=test_param)
        actual_output = thingspeak_builder.build_url()
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_building_thingspeak_url(self):
        test_param_missing_id = {'format': 'json', "api_key": "key", "opt": "val"}
        thingspeak_builder = URLBuilderThingspeak(api_address=self.api_address, parameters=test_param_missing_id)
        with self.assertRaises(SystemExit):
            thingspeak_builder.build_url()

        test_param_missing_format = {"channel_id": "id", "api_key": "key", "opt": "val"}
        thingspeak_builder = URLBuilderThingspeak(api_address=self.api_address, parameters=test_param_missing_format)
        with self.assertRaises(SystemExit):
            thingspeak_builder.build_url()

        test_param_missing_key = {"channel_id": "id", 'format': 'json', "opt": "val"}
        thingspeak_builder = URLBuilderThingspeak(api_address=self.api_address, parameters=test_param_missing_key)
        with self.assertRaises(SystemExit):
            thingspeak_builder.build_url()


if __name__ == '__main__':
    unittest.main()
