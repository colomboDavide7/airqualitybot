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
        self.dbfactory = Psycopg2ConnectionAdapterFactory()
        self.psycopg2_adapter    = self.dbfactory.create_database_connection_adapter(self.settings)

    def test_missing_setting_argument(self):
        """Test SystemExit when some setting argument is missing."""
        settings = {"port": 12345,
                    "dbname": "some_db_name"}
        with self.assertRaises(SystemExit):
            self.dbfactory.create_database_connection_adapter(settings)

    def test_system_exit_when_open_conn_with_invalid_arguments(self):
        """Test SystemExit when open connection with invalid database arguments."""
        with self.assertRaises(SystemExit):
            self.psycopg2_adapter.open_conn()

    def test_system_exit_close_conn(self):
        """
        Test SystemExit when try to close a connection that is not opened.
        """
        with self.assertRaises(SystemExit):
            self.psycopg2_adapter.close_conn()

    def test_system_exit_send(self):
        """Test SystemExit when try to send message through the connection but
        it is closed."""
        with self.assertRaises(SystemExit):
            self.psycopg2_adapter.send("some_sql_statement;")


if __name__ == '__main__':
    unittest.main()
