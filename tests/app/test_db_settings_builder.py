#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 16:40
# @Description: This script contains the unit tests for testing the building
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



if __name__ == '__main__':
    unittest.main()
