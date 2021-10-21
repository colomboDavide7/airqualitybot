#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 16:40
# @Description: This script contains the unit test for testing ResourcePicker.
#
#################################################

import unittest
from airquality.picker.resource_picker import ResourcePicker


class TestResourcePicker(unittest.TestCase):

    def test_pick_db_conn_properties_from_user(self):
        """Test picking database properties from user."""

        parsed_res = {"server": {"key1": "val1", "key2": "val2"},
                      "users": {"usr1": "pwd1", "usr2": "pwd2"}}
        expected_output = {"key1": "val1", "key2": "val2", "username": "usr1", "password": "pwd1"}
        actual_output = ResourcePicker.pick_db_conn_properties_from_user(parsed_res, "usr1")
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_missing_server_section(self):
        """Test SystemExit when 'server' section is not present in 'properties/resources.json'."""

        parsed_res = {"users": {}}
        with self.assertRaises(SystemExit):
            ResourcePicker.pick_db_conn_properties_from_user(parsed_res, "usr1")

    def test_system_exit_when_missing_users_section(self):
        """Test SystemExit when 'users' section is not present in 'properties/resources.json'"""

        parsed_res = {"servers": {}}
        with self.assertRaises(SystemExit):
            ResourcePicker.pick_db_conn_properties_from_user(parsed_res, "usr1")

    def test_pick_sensor_model_from_sensor_type(self):
        """Test picking all sensor models associated to a given sensor type."""

        parsed_res = {"models": {"mobile": ['model1', 'model2'],
                                 "station": ['model3', 'model4']}}

        expected_output = ["model1", "model2"]
        actual_output = ResourcePicker.pick_sensor_models_from_sensor_type(parsed_res, "mobile")
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_missing_models_section(self):
        """Test SystemExit when models section is missing in 'properties/resources.json'."""

        parsed_res = {"server": {"key1": "val1", "key2": "val2"},
                      "users": {"usr1": "pwd1", "usr2": "pwd2"}}

        with self.assertRaises(SystemExit):
            ResourcePicker.pick_sensor_models_from_sensor_type(parsed_res, "mobile")

    def test_system_exit_when_pass_invalid_sensor_type(self):
        """Test SystemExit when try to pick all sensor models with invalid sensor type."""

        parsed_res = {"models": {"mobile": ['model1', 'model2'],
                                 "station": ['model3', 'model4']}}

        with self.assertRaises(SystemExit):
            ResourcePicker.pick_sensor_models_from_sensor_type(parsed_res, "bad_sensor_type")


if __name__ == '__main__':
    unittest.main()
