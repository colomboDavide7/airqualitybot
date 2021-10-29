#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: unit test script
#
#################################################

import unittest
from airquality.api.url_querystring_builder import URLQuerystringBuilderFactory


class TestBuilder(unittest.TestCase):


    ################################ ATMOTUBE QUERYSTRING BUILDER TESTS ################################

    def test_successfully_build_atmotube_querystring(self):

        test_kwargs = {"api_key": "some_api_key", "mac": "some_mac_address",
                       "date": "2021-10-11 17:46:00", "order": "desc"}
        expected_querystring = "api_key=some_api_key&mac=some_mac_address&date=2021-10-11&order=desc"
        atmotube_builder = URLQuerystringBuilderFactory().create_querystring_builder(bot_personality = "atmotube")
        actual_querystring = atmotube_builder.make_querystring(parameters = test_kwargs)
        self.assertEqual(actual_querystring, expected_querystring)


    def test_system_exit_when_building_atmotube_querystring(self):
        """Test SystemExit when missing required parameters for building atmotube querystring."""

        test_kwargs = {"api_key": "some_api_key", "date": "2021-10-11 09:44:00"}
        atmotube_builder = URLQuerystringBuilderFactory().create_querystring_builder(bot_personality = "atmotube")
        with self.assertRaises(SystemExit):
            atmotube_builder.make_querystring(parameters = test_kwargs)

        test_kwargs = {"api_key": "some_api_key", "mac": "some_mac_address"}
        with self.assertRaises(SystemExit):
            atmotube_builder.make_querystring(parameters = test_kwargs)


################################ PURPLE AIR QUERYSTRING BUILDER TESTS ################################


    def test_successfully_build_purpleair_querystring(self):
        """Test the build of a valid purpleair URL querystring."""

        test_param = {"api_key": "key", "fields": ["f1", "f2"], "opt": "val"}
        expected_output = "api_key=key&fields=f1,f2&opt=val"
        purpleair_builder = URLQuerystringBuilderFactory().create_querystring_builder(bot_personality = "purpleair")
        actual_output = purpleair_builder.make_querystring(parameters = test_param)
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_when_building_purpleair_querystring(self):
        """Test SystemExit when missing required purpleair parameters for building URL querystring."""

        test_param = {"fields": "f1", "opt": "val"}
        purpleair_builder = URLQuerystringBuilderFactory().create_querystring_builder(bot_personality = "purpleair")
        with self.assertRaises(SystemExit):
            purpleair_builder.make_querystring(parameters = test_param)

        test_param = {"api_key": "key", "opt": "val"}
        with self.assertRaises(SystemExit):
            purpleair_builder.make_querystring(parameters = test_param)


################################ THING SPEAK QUERYSTRING BUILDER TESTS ################################


    def test_successfully_build_thingspeak_querystring(self):

        test_param = {'api_key': "key", 'start': 'ts1', 'end': 'ts2'}
        expected_output = "api_key=key&start=ts1&end=ts2"
        thingspeak_builder = URLQuerystringBuilderFactory.create_querystring_builder(bot_personality = "thingspeak")
        actual_output = thingspeak_builder.make_querystring(parameters = test_param)
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_when_missing_parameters_thingspeak_builder(self):

        test_param = {'start': 'ts1', 'end': 'ts2'}
        thingspeak_builder = URLQuerystringBuilderFactory.create_querystring_builder(bot_personality = "thingspeak")
        with self.assertRaises(SystemExit):
            thingspeak_builder.make_querystring(parameters = test_param)






if __name__ == '__main__':
    unittest.main()
