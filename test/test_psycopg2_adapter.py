######################################################
#
# Author: Davide Colombo
# Date: 20/12/21 09:11
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.dbadapter import Psycopg2DBAdapter, DatabaseAdapterError


TEST_DATABASE_RESPONSES = [("pkey1", "v1", "v2"), ("pkey2", "v3", "v4"), ("pkey3", "v5", "v6")]


class TestPsycopg2DBAdapter(TestCase):

    @property
    def mocked_cursor(self) -> MagicMock:
        mocked_cursor = MagicMock()
        mocked_cursor.__enter__.return_value = mocked_cursor
        mocked_cursor.fetchall.return_value = TEST_DATABASE_RESPONSES
        mocked_cursor.fetchone.side_effect = TEST_DATABASE_RESPONSES
        return mocked_cursor

    @property
    def mocked_conn(self) -> MagicMock:
        mocked_conn = MagicMock()
        mocked_conn.close.side_effect = [True, DatabaseAdapterError]
        mocked_conn.cursor.return_value = self.mocked_cursor
        return mocked_conn

    @patch('airquality.dbadapter.psycopg2.connect')
    def test_successfully_execute(self, mocked_connect):
        mocked_connect.return_value = self.mocked_conn

        with Psycopg2DBAdapter(dbname="fake_dbname", user="fake_user", password="fake_password") as adapter:
            print(repr(adapter))
            actual = adapter.execute("INSERT INTO ...")
            self.assertIsNone(actual)
            actual = adapter.execute("DELETE ...")
            self.assertIsNone(actual)

            with self.assertRaises(ValueError):
                adapter.execute("SOME QUERY THAT DO NOT STARTS WITH 'INSERT INTO' or 'DELETE'")

        with self.assertRaises(DatabaseAdapterError):
            adapter.close()

    @patch('airquality.dbadapter.psycopg2.connect')
    def test_successfully_fetchall(self, mocked_connect):
        mocked_connect.return_value = self.mocked_conn

        with Psycopg2DBAdapter(dbname="fake_dbname", user="fake_user", password="fake_password") as adapter:
            print(repr(adapter))
            actual = adapter.fetch_all("SELECT ...")
            self.assertEqual(actual, TEST_DATABASE_RESPONSES)

            with self.assertRaises(ValueError):
                adapter.fetch_all("SOME QUERY THAT DO NOT STARTS WITH 'SELECT'")

        with self.assertRaises(DatabaseAdapterError):
            adapter.close()

    @patch('airquality.dbadapter.psycopg2.connect')
    def test_successfully_fetchone(self, mocked_connect):
        mocked_connect.return_value = self.mocked_conn

        with Psycopg2DBAdapter(dbname="fake_dbname", user="fake_user", password="fake_password") as adapter:
            print(repr(adapter))
            actual = adapter.fetch_one("SELECT ...")
            self.assertEqual(actual, TEST_DATABASE_RESPONSES[0])
            actual = adapter.fetch_one("SELECT ...")
            self.assertEqual(actual, TEST_DATABASE_RESPONSES[1])
            actual = adapter.fetch_one("SELECT ...")
            self.assertEqual(actual, TEST_DATABASE_RESPONSES[2])

            with self.assertRaises(ValueError):
                adapter.fetch_one("SOME QUERY THAT DO NOT STARTS WITH 'SELECT'")

        with self.assertRaises(DatabaseAdapterError):
            adapter.close()


if __name__ == '__main__':
    main()
