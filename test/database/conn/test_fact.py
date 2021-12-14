######################################################
#
# Author: Davide Colombo
# Date: 29/11/21 20:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.conn.fact as fact
import database.conn as adapt
import airquality.database.conn.shutdown as shut


class TestDatabaseConn(unittest.TestCase):

    def test_successfully_get_database_adapter(self):
        actual = fact.get_database_adapter(connection_string="some_connection_string", adapter_type="psycopg2")
        self.assertEqual(actual.__class__, adapt.Psycopg2DBConn)

    def test_exit_on_bad_adapter_type(self):
        with self.assertRaises(SystemExit):
            fact.get_database_adapter(
                connection_string="some_connection_string", adapter_type="bad adapter type"
            )

    def test_successfully_shutdown_database(self):
        shut.shutdown()
        self.assertEqual(len(shut.ACTIVE_CONNECTIONS), 0)


if __name__ == '__main__':
    unittest.main()
