#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 12:34
# @Description: unit test script
#
#################################################

import unittest
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory


class TestDatabaseConnectionAdapter(unittest.TestCase):


    def setUp(self) -> None:
        self.settings = {"port": 12345, "dbname": "some_db_name", "host": "some_host_name",
                         "username": "some_user_name", "password": "some_password"}
        self.psycopg2_adapter    = Psycopg2ConnectionAdapterFactory().create_database_connection_adapter(self.settings)


    def test_missing_setting_argument(self):
        """Test SystemExit when some setting argument is missing."""

        test_settings = {"port": 12345, "dbname": "some_db_name"}

        with self.assertRaises(SystemExit):
            Psycopg2ConnectionAdapterFactory().create_database_connection_adapter(test_settings)


    def test_system_exit_when_opening_connection_with_wrong_settings(self):
        """Test SystemExit when open connection with invalid database settings."""

        with self.assertRaises(SystemExit):
            self.psycopg2_adapter.open_conn()


    def test_system_exit_when_closing_connection(self):
        """Test SystemExit when try to close a connection that is not opened."""

        with self.assertRaises(SystemExit):
            self.psycopg2_adapter.close_conn()


    def test_system_exit_when_sending_invalid_executable_query(self):
        """Test SystemExit when try to send message through the connection but it is closed."""

        with self.assertRaises(SystemExit):
            self.psycopg2_adapter.send("some_sql_statement;")


if __name__ == '__main__':
    unittest.main()
