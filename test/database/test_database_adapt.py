######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 15:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import psycopg2
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.database.adapter import Psycopg2Adapter, DatabaseError


class TestDatabaseAdapter(TestCase):

    @property
    def get_test_connection_properties(self):
        return {'dbname': 'fakedbname', 'user': 'fakeuser', 'password': 'fakepassword', 'host': 'fakehost',
                'port': 'fakeport'}

    ##################################### test_fetchone #####################################
    @patch('airquality.database.adapter.connect')
    def test_fetchone(self, mocked_connect):
        mocked_cursor = MagicMock()
        mocked_cursor.__enter__.return_value = mocked_cursor
        mocked_cursor.execute = MagicMock()
        mocked_cursor.fetchone.return_value = ("some value",)
        mocked_conn = MagicMock()
        mocked_conn.cursor.return_value = mocked_cursor
        mocked_connect.return_value = mocked_conn

        test_query = "query."
        with Psycopg2Adapter(**self.get_test_connection_properties) as adapter:
            actual = adapter.fetchone(test_query)
        mocked_cursor.execute.assert_called_with(test_query)
        self.assertEqual(actual[0], "some value")

    ##################################### test_fetchall #####################################
    @patch('airquality.database.adapter.connect')
    def test_fetchall(self, mocked_connect):
        mocked_cursor = MagicMock()
        mocked_cursor.__enter__.return_value = mocked_cursor
        mocked_cursor.execute = MagicMock()
        mocked_cursor.fetchall.return_value = [("row1",), ("row2",)]

        mocked_conn = MagicMock()
        mocked_conn.cursor.return_value = mocked_cursor
        mocked_connect.return_value = mocked_conn

        test_query = "query."
        with Psycopg2Adapter(**self.get_test_connection_properties) as adapter:
            actual = adapter.fetchall(test_query)

        mocked_cursor.execute.assert_called_with(test_query)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0], ("row1",))
        self.assertEqual(actual[1], ("row2",))

    ##################################### test_execute #####################################
    @patch('airquality.database.adapter.connect')
    def test_execute(self, mocked_connect):
        mocked_cursor = MagicMock()
        mocked_cursor.__enter__.return_value = mocked_cursor
        mocked_cursor.execute = MagicMock()
        mocked_cursor.fetchall.return_value = [("row1",), ("row2",)]

        mocked_conn = MagicMock()
        mocked_conn.cursor.return_value = mocked_cursor
        mocked_conn.close = MagicMock()
        mocked_connect.return_value = mocked_conn

        test_query = "query."
        with Psycopg2Adapter(**self.get_test_connection_properties) as adapter:
            adapter.execute(test_query)
        mocked_cursor.execute.assert_called_with(test_query)
        mocked_conn.close.assert_called_once()

    ##################################### test_close_connection #####################################
    @patch('airquality.database.adapter.connect')
    def test_exit_on_psycopg2_Error(self, mocked_connect):
        mocked_cursor = MagicMock()
        mocked_cursor.__enter__.return_value = mocked_cursor
        mocked_cursor.execute.side_effect = [psycopg2.Error("psycopg2 error")]

        mocked_conn = MagicMock()
        mocked_conn.close = MagicMock()
        mocked_conn.cursor.return_value = mocked_cursor
        mocked_connect.return_value = mocked_conn

        with self.assertRaises(DatabaseError):
            with Psycopg2Adapter(**self.get_test_connection_properties) as adapter:
                adapter.execute(query="some query.")
            mocked_conn.close.assert_called_once()


if __name__ == '__main__':
    main()
