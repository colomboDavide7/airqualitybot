#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: unit test script
#
#################################################

from airquality.api.url_querystring_builder import URLQuerystringBuilder
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

    def test_build_purpleair_querystring(self):
        test_param = {"api_key": "key", "fields": ["f1", "f2"], "opt": "val"}
        expected_output = "api_key=key&fields=f1,f2&opt=val"
        actual_output = URLQuerystringBuilder.PA_querystring_from_fields(api_param = test_param)
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_when_fields_is_not_a_list_build_purpleair_querystring(self):

        test_param = {"api_key": "key", "fields": "f1", "opt": "val"}
        with self.assertRaises(SystemExit):
            URLQuerystringBuilder.PA_querystring_from_fields(api_param = test_param)

    def test_missing_parameters_build_purpleair_querystring(self):

        test_param = {"fields": "f1", "opt": "val"}
        with self.assertRaises(SystemExit):
            URLQuerystringBuilder.PA_querystring_from_fields(api_param = test_param)

        test_param = {"api_key": "key", "opt": "val"}
        with self.assertRaises(SystemExit):
            URLQuerystringBuilder.PA_querystring_from_fields(api_param = test_param)


if __name__ == '__main__':
    unittest.main()
