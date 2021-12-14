######################################################
#
# Author: Davide Colombo
# Date: 29/11/21 20:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.conn as adapt


class TestDatabaseConn(unittest.TestCase):

    def test_exit_on_bad_adapter_type(self):
        with self.assertRaises(SystemExit):
            adapt.Psycopg2DBConn(connection_string="some_connection_string")

    def test_successfully_shutdown_database(self):
        adapt.shutdown()
        self.assertEqual(len(adapt.ACTIVE_CONNECTIONS), 0)


if __name__ == '__main__':
    unittest.main()
