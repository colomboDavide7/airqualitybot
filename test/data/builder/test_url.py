#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: unit test script
#
#################################################
import unittest
import airquality.data.builder.url as url


class TestURLBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.api_address = 'some_api_address'

    def test_successfully_build_purpleair_url(self):
        test_param = {"api_key": "key", "fields": ["f1", "f2"], "opt": "val"}
        expected_output = "some_api_address?api_key=key&fields=f1,f2&opt=val"
        purpleair_builder = url.PurpleairURLBuilder(api_address=self.api_address, parameters=test_param)
        actual_output = purpleair_builder.url()
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_building_purpleair_url(self):
        test_param_missing_key = {"fields": ["f1", "f2"], "opt": "val"}
        with self.assertRaises(SystemExit):
            url.PurpleairURLBuilder(api_address=self.api_address, parameters=test_param_missing_key)

        test_param_missing_fields = {"api_key": "some_key", "opt": "val"}
        with self.assertRaises(SystemExit):
            url.PurpleairURLBuilder(api_address=self.api_address, parameters=test_param_missing_fields)

        test_param_empty_fields = {"api_key": "some_key", "fields": [], "opt": "val"}
        builder = url.PurpleairURLBuilder(api_address=self.api_address, parameters=test_param_empty_fields)
        with self.assertRaises(SystemExit):
            builder.url()

    ################################ TEST BUILD ATMOTUBE URL ################################
    def test_successfully_build_atmotube_url(self):
        test_param = {"api_key": "key", 'mac': 'some_mac', "opt": "val"}
        expected_output = "some_api_address?api_key=key&mac=some_mac&opt=val"
        atmotube_builder = url.AtmotubeURLBuilder(api_address=self.api_address, parameters=test_param)
        actual_output = atmotube_builder.url()
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_building_atmotube_url(self):
        test_param_missing_key = {'mac': 'some_mac', "opt": "val"}
        with self.assertRaises(SystemExit):
            url.AtmotubeURLBuilder(api_address=self.api_address, parameters=test_param_missing_key)

        test_param_missing_mac = {"api_key": "key", "opt": "val"}
        with self.assertRaises(SystemExit):
            url.AtmotubeURLBuilder(api_address=self.api_address, parameters=test_param_missing_mac)

    def test_build_atmotube_url_with_different_datatype(self):
        test_param = {"api_key": "key", 'mac': 'some_mac', "opt_num": 10, "opt_bool": True}
        expected_output = "some_api_address?api_key=key&mac=some_mac&opt_num=10&opt_bool=True"
        atmotube_builder = url.AtmotubeURLBuilder(api_address=self.api_address, parameters=test_param)
        actual_output = atmotube_builder.url()
        self.assertEqual(actual_output, expected_output)

    ################################ TEST BUILD THINGSPEAK URL ################################
    def test_successfully_build_thingspeak_url(self):
        test_param = {"channel_id": "id", 'format': 'json', "api_key": "key", "opt": "val"}
        expected_output = "some_api_address/id/feeds.json?api_key=key&opt=val"
        thingspeak_builder = url.ThingspeakURLBuilder(api_address=self.api_address, parameters=test_param)
        actual_output = thingspeak_builder.url()
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_building_thingspeak_url(self):
        test_param_missing_id = {'format': 'json', "api_key": "key", "opt": "val"}
        with self.assertRaises(SystemExit):
            url.ThingspeakURLBuilder(api_address=self.api_address, parameters=test_param_missing_id)

        test_param_missing_format = {"channel_id": "id", "api_key": "key", "opt": "val"}
        with self.assertRaises(SystemExit):
            url.ThingspeakURLBuilder(api_address=self.api_address, parameters=test_param_missing_format)

        test_param_missing_key = {"channel_id": "id", 'format': 'json', "opt": "val"}
        with self.assertRaises(SystemExit):
            url.ThingspeakURLBuilder(api_address=self.api_address, parameters=test_param_missing_key)

    def test_build_thingspeak_url_with_different_datatype(self):
        test_param = {"channel_id": "id", 'format': 'json', "api_key": "key", "opt_num": 10, "opt_bool": True}
        expected_output = "some_api_address/id/feeds.json?api_key=key&opt_num=10&opt_bool=True"
        thingspeak_builder = url.ThingspeakURLBuilder(api_address=self.api_address, parameters=test_param)
        actual_output = thingspeak_builder.url()
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
