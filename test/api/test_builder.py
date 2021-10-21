#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: This script contains all the test of the 'api.builder' module
#
#################################################

from airquality.api.builder import URLQuerystringBuilder
import unittest

class TestBuilder(unittest.TestCase):

    def test_atmotube_querystring_from_date(self):
        """Test build atmotube querystring from date."""

        test_kwargs = {"api_key": "some_api_key",
                       "mac": "some_mac_address",
                       "date": "2021-10-11",
                       "order": "desc"}
        expected_querystring = \
            "api_key=some_api_key&mac=some_mac_address&date=2021-10-11&order=desc"

        actual_querystring = \
            URLQuerystringBuilder.AT_querystring_from_date(test_kwargs)
        self.assertEqual(actual_querystring, expected_querystring)

    def test_ignore_atmotube_from_date(self):
        """Test build atmotube querystring from date with invalid arguments."""

        test_kwargs = {"api_key": "some_api_key",
                       "mac": "some_mac_address",
                       "date": "2021-10-11",
                       "ciao": "ignored"}
        expected_querystring = \
            "api_key=some_api_key&mac=some_mac_address&date=2021-10-11"

        actual_querystring = \
            URLQuerystringBuilder.AT_querystring_from_date(test_kwargs)
        self.assertEqual(actual_querystring, expected_querystring)

    def test_system_exit_atmotube_from_date(self):
        test_kwargs = {"api_key": "some_api_key",
                       "date": "2021-10-11",
                       "ciao": "ignored"}

        with self.assertRaises(SystemExit):
            URLQuerystringBuilder.AT_querystring_from_date(test_kwargs)

        test_kwargs = {"api_key": "some_api_key",
                       "mac": "some_mac_address",
                       "ciao": "ignored"}
        with self.assertRaises(SystemExit):
            URLQuerystringBuilder.AT_querystring_from_date(test_kwargs)

if __name__ == '__main__':
    unittest.main()
