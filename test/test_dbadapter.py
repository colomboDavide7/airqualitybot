######################################################
#
# Author: Davide Colombo
# Date: 20/12/21 09:11
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
from airquality.dbadapterabc import DBAdapterABC


class MockDBAdapter(DBAdapterABC):

    def __init__(self):
        self.flag_calls = []
        self.conn = True

    def process_query(self, query: str, fetchone=False, execute=False):
        self.flag_calls.append((fetchone, execute))

    def close(self):
        self.conn = False


class TestDBAdapter(unittest.TestCase):

    def test_successfully_process_query(self):
        with MockDBAdapter() as db:
            db.execute("INSERT INTO ... ")
            db.fetch_all("SELECT ...")
            db.fetch_one("SELECT ...")
            db.fetch_one("SELECT ...")
            db.execute("DELETE ...")

        expected = [(False, True), (False, False), (True, False), (True, False), (False, True)]
        self.assertEqual(db.flag_calls, expected)
        self.assertFalse(db.conn)

    def test_execute_ValueError(self):
        with self.assertRaises(ValueError):
            with MockDBAdapter() as db:
                db.execute("SELECT ... ")
        self.assertFalse(db.conn)

    def test_fetch_all_ValueError(self):
        with self.assertRaises(ValueError):
            with MockDBAdapter() as db:
                db.fetch_all("INSERT INTO")

        with self.assertRaises(ValueError):
            with MockDBAdapter() as db:
                db.fetch_all("DELETE")
        self.assertFalse(db.conn)

    def test_fetch_one_ValueError(self):
        with self.assertRaises(ValueError):
            with MockDBAdapter() as db:
                db.fetch_one("INSERT INTO")

        with self.assertRaises(ValueError):
            with MockDBAdapter() as db:
                db.fetch_one("DELETE")
        self.assertFalse(db.conn)


if __name__ == '__main__':
    unittest.main()
