#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: unit test script
#
#################################################
import unittest
import airquality.api.util.url as url


class TestURLBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.address = 'some_api_address'

    def test_successfully_build_purpleair_url(self):
        test_param = {"api_key": "key", "fields": ["f1", "f2"], "opt": "val"}
        expected_output = "some_api_address?fields=f1,f2&api_key=key&opt=val"
        purpleair_builder = url.PurpleairURL(address=self.address, url_param=test_param)
        actual_output = purpleair_builder.url()
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_purpleair_api_key(self):
        test_param_missing_key = {"fields": ["f1", "f2"], "opt": "val"}
        url_builder = url.PurpleairURL(address=self.address, url_param=test_param_missing_key)
        with self.assertRaises(SystemExit):
            url_builder.url()

    def test_exit_on_missing_purpleair_fields(self):
        test_param_missing_fields = {"api_key": "some_key", "opt": "val"}
        url_builder = url.PurpleairURL(address=self.address, url_param=test_param_missing_fields)
        with self.assertRaises(SystemExit):
            url_builder.url()

    def test_exit_on_empty_fields(self):
        test_param_empty_fields = {"api_key": "some_key", "fields": [], "opt": "val"}
        builder = url.PurpleairURL(address=self.address, url_param=test_param_empty_fields)
        with self.assertRaises(SystemExit):
            builder.url()

    ################################ TEST BUILD ATMOTUBE URL ################################
    def test_successfully_build_atmotube_url(self):
        test_param = {"api_key": "key", 'mac': 'some_mac', "opt": "val"}
        expected_output = "some_api_address?api_key=key&mac=some_mac&opt=val"
        atmotube_builder = url.AtmotubeURL(address=self.address, url_param=test_param)
        actual_output = atmotube_builder.url()
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_atmotube_api_key(self):
        test_param_missing_key = {'mac': 'some_mac', "opt": "val"}
        url_builder = url.AtmotubeURL(address=self.address, url_param=test_param_missing_key)
        with self.assertRaises(SystemExit):
            url_builder.url()

    def test_exit_on_missing_atmotube_mac_address(self):
        test_param_missing_mac = {"api_key": "key", "opt": "val"}
        url_builder = url.AtmotubeURL(address=self.address, url_param=test_param_missing_mac)
        with self.assertRaises(SystemExit):
            url_builder.url()

    def test_build_atmotube_url_with_different_datatype(self):
        test_param = {"api_key": "key", 'mac': 'some_mac', "opt_num": 10, "opt_bool": True}
        expected_output = "some_api_address?api_key=key&mac=some_mac&opt_num=10&opt_bool=True"
        atmotube_builder = url.AtmotubeURL(address=self.address, url_param=test_param)
        actual_output = atmotube_builder.url()
        self.assertEqual(actual_output, expected_output)

    ################################ TEST BUILD THINGSPEAK URL ################################
    def test_successfully_build_thingspeak_url(self):
        test_param = {"channel_id": "id", 'format': 'json', "api_key": "key", "opt": "val", "start": "d t"}
        expected_output = "some_api_address/id/feeds.json?api_key=key&opt=val&start=d%20t"
        thingspeak_builder = url.ThingspeakURL(address=self.address, url_param=test_param)
        actual_output = thingspeak_builder.url()
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_thingspeak_channel_id(self):
        test_param_missing_id = {'format': 'json', "api_key": "key", "opt": "val"}
        url_builder = url.ThingspeakURL(address=self.address, url_param=test_param_missing_id)
        with self.assertRaises(SystemExit):
            url_builder.url()

    def test_exit_on_missing_thingspeak_response_format(self):
        test_param_missing_format = {"channel_id": "id", "api_key": "key", "opt": "val"}
        with self.assertRaises(SystemExit):
            url.ThingspeakURL(address=self.address, url_param=test_param_missing_format)

    def test_exit_on_missing_thingspeak_channel_key(self):
        test_param_missing_key = {"channel_id": "id", 'format': 'json', "opt": "val"}
        url_builder = url.ThingspeakURL(address=self.address, url_param=test_param_missing_key)
        with self.assertRaises(SystemExit):
            url_builder.url()

    def test_build_thingspeak_url_with_different_datatype(self):
        test_param = {"channel_id": "id", 'format': 'json', "api_key": "key", "opt_num": 10, "opt_bool": True}
        expected_output = "some_api_address/id/feeds.json?api_key=key&opt_num=10&opt_bool=True"
        thingspeak_builder = url.ThingspeakURL(address=self.address, url_param=test_param)
        actual_output = thingspeak_builder.url()
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
