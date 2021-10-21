#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 16:40
# @Description: This script contains the unit test for testing the building
#               of the setting dictionary for opening connection with database.
#
#################################################

import unittest
from airquality.app.db_settings_builder import DatabaseSettingsBuilder


class TestDatabaseSettingsBuilder(unittest.TestCase):
    """Test class for DatabaseSettingsBuilder class."""

    def test_build_database_settings(self):
        """Test building database settings."""

        parsed_res = {"server": {"key1": "val1", "key2": "val2"},
                      "users": {"usr1": "pwd1", "usr2": "pwd2"}}
        expected_output = {"key1": "val1", "key2": "val2", "username": "usr1", "password": "pwd1"}
        actual_output = DatabaseSettingsBuilder.create_db_settings_from_parsed_resources_for_user(parsed_res, "usr1")
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_missing_server_section(self):
        """Test SystemExit when 'server' section is not present in parsed
        resources."""

        parsed_res = {"users": {}}
        with self.assertRaises(SystemExit):
            DatabaseSettingsBuilder.create_db_settings_from_parsed_resources_for_user(parsed_res, "usr1")

    def test_system_exit_missing_users_section(self):
        """Test SystemExit when 'users' section is not present in parsed
        resources."""

        parsed_res = {"servers": {}}
        with self.assertRaises(SystemExit):
            DatabaseSettingsBuilder.create_db_settings_from_parsed_resources_for_user(
                parsed_res, "usr1")

    def test_sensor_model_by_type(self):
        """Test get list of sensor model from sensor type."""

        parsed_res = {"models": {"mobile": ['model1', 'model2'],
                                 "station": ['model3', 'model4']}}

        expected_output = ["model1", "model2"]
        actual_output = DatabaseSettingsBuilder.list_models_from_type(parsed_res, "mobile")
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_sensor_model_by_type(self):
        """Test SystemExit when sensor model section is missing in resource file."""

        parsed_res = {"server": {"key1": "val1", "key2": "val2"},
                      "users": {"usr1": "pwd1", "usr2": "pwd2"}}

        with self.assertRaises(SystemExit):
            DatabaseSettingsBuilder.list_models_from_type(parsed_res, "mobile")

    def test_system_exit_invalid_sensor_type(self):
        """Test SystemExit when try to get list of sensor models by invalid type."""
        parsed_res = {"models": {"mobile": ['model1', 'model2'],
                                 "station": ['model3', 'model4']}}

        with self.assertRaises(SystemExit):
            DatabaseSettingsBuilder.list_models_from_type(parsed_res, "bad_sensor_type")


if __name__ == '__main__':
    unittest.main()
