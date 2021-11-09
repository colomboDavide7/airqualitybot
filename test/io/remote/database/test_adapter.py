#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 12:34
# @Description: unit test script
#
#################################################

import unittest
import airquality.io.remote.database.adapter as adpt


class TestDatabaseConnectionAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.bad_settings = {"port": 12345,
                             "dbname": "some_db_name",
                             "host": "some_host_name",
                             "username": "some_user_name",
                             "password": "some_password"}
        self.database_adapter = adpt.Psycopg2DatabaseAdapter(self.bad_settings)

    def test_system_exit_when_key_error_is_raised(self):
        test_settings = {"port": 12345, "dbname": "some_db_name"}
        with self.assertRaises(SystemExit):
            adpt.Psycopg2DatabaseAdapter(test_settings)

    def test_system_exit_when_opening_connection_with_wrong_settings(self):
        with self.assertRaises(SystemExit):
            self.database_adapter.open_conn()

    def test_system_exit_when_closing_connection_that_is_not_open(self):
        with self.assertRaises(SystemExit):
            self.database_adapter.close_conn()

    def test_system_exit_when_sending_invalid_executable_query(self):
        self.database_adapter.conn = "some object that is not None"
        with self.assertRaises(SystemExit):
            self.database_adapter.send("some_sql_statement;")


if __name__ == '__main__':
    unittest.main()
