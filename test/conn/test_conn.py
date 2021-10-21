#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 12:34
# @Description: This script is used for testing conn class behaviour
#
#################################################

import unittest
from airquality.conn.conn import DatabaseConnectionFactory


class TestConnection(unittest.TestCase):


    def setUp(self) -> None:
        self.settings = {"port": 12345, "dbname": "some_db_name", "host": "some_host_name",
                         "username": "some_user_name", "password": "some_password"}
        self.dbfactory = DatabaseConnectionFactory()
        self.dbconn    = self.dbfactory.create_connection(self.settings)

    def test_missing_setting_argument(self):
        """Test SystemExit when some setting argument is missing."""
        settings = {"port": 12345,
                    "dbname": "some_db_name"}
        with self.assertRaises(SystemExit):
            self.dbfactory.create_connection(settings)

    def test_system_exit_when_open_conn_with_invalid_arguments(self):
        """Test SystemExit when open connection with invalid database arguments."""
        with self.assertRaises(SystemExit):
            self.dbconn.open_conn()

    def test_system_exit_close_conn(self):
        """
        Test SystemExit when try to close a connection that is not opened.
        """
        with self.assertRaises(SystemExit):
            self.dbconn.close_conn()

    def test_system_exit_send(self):
        """Test SystemExit when try to send message through the connection but
        it is closed."""
        with self.assertRaises(SystemExit):
            self.dbconn.send("some_sql_statement;")


if __name__ == '__main__':
    unittest.main()
