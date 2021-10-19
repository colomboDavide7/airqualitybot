#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 12:34
# @Description: This script is used for testing conn class behaviour
#
#################################################

import unittest
from airquality.conn.conn import DatabaseConnection, DatabaseConnectionFactory


class TestConnection(unittest.TestCase):


    def setUp(self) -> None:
        self.settings = {"port": 5432,
                         "dbname": "airquality",
                         "host": "localhost",
                         "username": "bot_mobile_user",
                         "password": None}
        self.dbfactory = DatabaseConnectionFactory()
        self.dbconn    = self.dbfactory.create_connection(self.settings)

    def tearDown(self) -> None:
        if self.dbconn.is_open():
            self.dbconn.close_conn()

    def test_create_database_connection(self):
        """This method tests the creation of a DatabaseConnection instance."""

        self.assertIsInstance(self.dbfactory, DatabaseConnectionFactory)
        self.assertIsNotNone(self.dbconn)
        self.assertIsInstance(self.dbconn, DatabaseConnection)

    def test_missing_setting_argument(self):
        """Test SystemExit when some setting argument is missing."""
        settings = {"port": 5432,
                    "dbname": "airquality"}
        with self.assertRaises(SystemExit):
            self.dbfactory.create_connection(settings)

    def test_open_connection(self):
        """Test that the connection opens successfully."""
        response = self.dbconn.open_conn()
        self.assertTrue(response)

    def test_close_conn(self):
        """Test close connection."""
        response = self.dbconn.open_conn()
        self.assertTrue(response)
        response = self.dbconn.close_conn()
        self.assertTrue(response)
        self.assertFalse(self.dbconn.is_open())

    def test_system_exit_open_conn(self):
        """
        Test SystemExit when try to open a connection that is already opened.
        """
        response = self.dbconn.open_conn()
        self.assertTrue(response)
        with self.assertRaises(SystemExit):
            self.dbconn.open_conn()

    def test_system_exit_close_conn(self):
        """
        Test SystemExit when try to close a connection that is not opened.
        """
        with self.assertRaises(SystemExit):
            self.dbconn.close_conn()


if __name__ == '__main__':
    unittest.main()
