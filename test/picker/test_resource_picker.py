#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 16:40
# @Description: unit test script
#
#################################################

import unittest
from airquality.picker.resource_picker import ResourcePicker


class TestResourcePicker(unittest.TestCase):

    def test_pick_db_conn_properties_from_personality(self):
        """Test picking database properties from user."""

        parsed_res = {"server": {"key1": "val1", "key2": "val2"},
                      "personality": {
                          "pers1": {"username": "usr1", "password": "pwd1"}
                      }}


        expected_output = {"key1": "val1", "key2": "val2", "username": "usr1", "password": "pwd1"}
        actual_output = ResourcePicker.pick_db_conn_properties(parsed_res, "pers1")
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_missing_server_section(self):
        """Test SystemExit when 'server' section is missing from 'properties/resources.json'."""

        parsed_res = {"personality": {}}
        with self.assertRaises(SystemExit):
            ResourcePicker.pick_db_conn_properties(parsed_res, "pers1")

    def test_system_exit_when_missing_personality_section(self):
        """Test SystemExit when 'users' section is missing from 'properties/resources.json'"""

        parsed_res = {"servers": {}}
        with self.assertRaises(SystemExit):
            ResourcePicker.pick_db_conn_properties(parsed_res, "pers1")

    def test_pick_api_address_from_number(self):
        parsed_res = {"api_address": {
                          "pers1": {"1": "api_address_1", "2": "api_address_2"}
                      }}
        expected_output = "api_address_1"
        actual_output = ResourcePicker.pick_api_address_from_number(
                parsed_resources = parsed_res,
                bot_personality = "pers1",
                api_address_number = "1"
        )

        self.assertEqual(actual_output, expected_output)

    def test_system_exit_missing_api_address_section(self):
        parsed_res = {}
        with self.assertRaises(SystemExit):
            ResourcePicker.pick_api_address_from_number(
                    parsed_resources = parsed_res,
                    bot_personality = "pers1",
                    api_address_number = "1"
            )

    def test_system_exit_when_wrong_personality_is_passed(self):
        parsed_res = {"api_address": {
            "pers1": {"1": "api_address_1", "2": "api_address_2"}
        }}

        with self.assertRaises(SystemExit):
            ResourcePicker.pick_api_address_from_number(
                    parsed_resources = parsed_res,
                    bot_personality = "bad_personality",
                    api_address_number = "1"
            )

    def test_system_exit_when_wrong_api_number(self):
        parsed_res = {"api_address": {
            "pers1": {"1": "api_address_1", "2": "api_address_2"}
        }}

        with self.assertRaises(SystemExit):
            ResourcePicker.pick_api_address_from_number(
                    parsed_resources = parsed_res,
                    bot_personality = "pers1",
                    api_address_number = "4"
            )



if __name__ == '__main__':
    unittest.main()
