#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 10:41
# @Description: unit test script
#
#################################################


import unittest
from airquality.api.api_address_formatter import APIAddressFormatterFactory
from airquality.constants.shared_constants import PURPLEAIR_CH_ID_PARAM

class TestAPIAddressFormatter(unittest.TestCase):


    def test_successfully_format_purpleair_api_address(self):

        test_fmt = {PURPLEAIR_CH_ID_PARAM: "123456"}
        test_address = "https://www.somesite.com/channels/{channel_id}/format.json"
        expected_output = "https://www.somesite.com/channels/123456/format.json"
        formatter = APIAddressFormatterFactory().create_api_address_formatter(bot_personality = "purpleair")
        formatter.raw_address = test_address
        actual_output = formatter.format_address(api_address_number = "2", fmt = test_fmt)
        self.assertEqual(actual_output, expected_output)


    def test_system_exit_when_raw_address_is_none_purpleair_formatter(self):

        test_fmt = {PURPLEAIR_CH_ID_PARAM: "123456"}
        formatter = APIAddressFormatterFactory().create_api_address_formatter(bot_personality = "purpleair")
        with self.assertRaises(SystemExit):
            formatter.format_address(api_address_number = "2", fmt = test_fmt)


    def test_system_exit_when_missing_formatter_key_purpleair_formatter(self):

        test_fmt = {"bad_formatter_key": "123456"}
        test_address = "https://www.somesite.com/channels/{channel_id}/format.json"
        formatter = APIAddressFormatterFactory().create_api_address_formatter(bot_personality = "purpleair")
        formatter.raw_address = test_address
        with self.assertRaises(SystemExit):
            formatter.format_address(api_address_number = "2", fmt = test_fmt)


    def test_raw_address_when_formatting_purpleair_address(self):

        test_fmt = {PURPLEAIR_CH_ID_PARAM: "123456"}
        test_address = "https://www.somesite.com/sensors/v1/"
        expected_output = "https://www.somesite.com/sensors/v1/"
        formatter = APIAddressFormatterFactory().create_api_address_formatter(bot_personality = "purpleair")
        formatter.raw_address = test_address
        actual_output = formatter.format_address(api_address_number = "1", fmt = test_fmt)
        self.assertEqual(actual_output, expected_output)



################################ DEFAULT FORMATTER TESTS ################################


    def test_successfully_format_api_address_default_formatter(self):

        test_address = "some_api_address"
        expected_output = "some_api_address"
        formatter = APIAddressFormatterFactory().create_api_address_formatter(bot_personality = "atmotube")
        formatter.raw_address = test_address
        actual_output = formatter.format_address(api_address_number = "", fmt = {"some": "val"})
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_missing_raw_address_default_formatter(self):

        test_fmt = {PURPLEAIR_CH_ID_PARAM: "123456"}
        formatter = APIAddressFormatterFactory().create_api_address_formatter(bot_personality = "purpleair")
        with self.assertRaises(SystemExit):
            formatter.format_address(api_address_number = "", fmt = test_fmt)



if __name__ == '__main__':
    unittest.main()
