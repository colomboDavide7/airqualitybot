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


    def setUp(self) -> None:
        """Every time a test is run, create the builders."""
        self.factory = URLQuerystringBuilderFactory()


################################ ATMOTUBE QUERYSTRING BUILDER TESTS ################################


    def test_atmotube_querystring_from_date(self):
        """Test build atmotube querystring from date."""

        test_kwargs = {"api_key": "some_api_key", "mac": "some_mac_address",
                       "date": "2021-10-11", "order": "desc"}
        expected_querystring = "api_key=some_api_key&mac=some_mac_address&date=2021-10-11&order=desc"
        atmotube_builder = self.factory.create_querystring_builder(bot_personality = "atmotube")
        actual_querystring = atmotube_builder.make_querystring(parameters = test_kwargs)
        self.assertEqual(actual_querystring, expected_querystring)


    def test_ignore_atmotube_from_date(self):
        """Test build atmotube querystring from date with invalid arguments."""

        test_kwargs = {"api_key": "some_api_key",
                       "mac": "some_mac_address",
                       "date": "2021-10-11",
                       "ciao": "ignored"}
        expected_querystring = "api_key=some_api_key&mac=some_mac_address&date=2021-10-11"
        atmotube_builder = self.factory.create_querystring_builder(bot_personality = "atmotube")
        actual_querystring = atmotube_builder.make_querystring(parameters = test_kwargs)
        self.assertEqual(actual_querystring, expected_querystring)


    def test_system_exit_atmotube_from_date(self):
        """Test SystemExit when missing required parameters for building atmotube querystring."""

        test_kwargs = {"api_key": "some_api_key",
                       "date": "2021-10-11",
                       "ciao": "ignored"}
        atmotube_builder = self.factory.create_querystring_builder(bot_personality = "atmotube")
        with self.assertRaises(SystemExit):
            atmotube_builder.make_querystring(parameters = test_kwargs)

        test_kwargs = {"api_key": "some_api_key",
                       "mac": "some_mac_address",
                       "ciao": "ignored"}
        with self.assertRaises(SystemExit):
            atmotube_builder.make_querystring(parameters = test_kwargs)


################################ PURPLE AIR QUERYSTRING BUILDER TESTS ################################


    def test_build_purpleair_querystring(self):
        """Test the build of a valid purpleair URL querystring."""

        test_param = {"api_key": "key", "fields": ["f1", "f2"], "opt": "val"}
        expected_output = "api_key=key&fields=f1,f2&opt=val"
        purpleair_builder = self.factory.create_querystring_builder(bot_personality = "purpleair")
        actual_output = purpleair_builder.make_querystring(parameters = test_param)
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_missing_parameters_build_purpleair_querystring(self):
        """Test SystemExit when missing required purple air parameters."""

        test_param = {"fields": "f1", "opt": "val"}
        purpleair_builder = self.factory.create_querystring_builder(bot_personality = "purpleair")
        with self.assertRaises(SystemExit):
            purpleair_builder.make_querystring(parameters = test_param)

        test_param = {"api_key": "key", "opt": "val"}
        with self.assertRaises(SystemExit):
            purpleair_builder.make_querystring(parameters = test_param)



if __name__ == '__main__':
    unittest.main()
