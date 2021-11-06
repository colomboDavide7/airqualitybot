#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:32
# @Description: unit test script
#
#################################################
import unittest
from airquality.database.sql_query_builder import SQLQueryBuilder


class TestSQLQueryBuilder(unittest.TestCase):

    def test_system_exit_when_query_identifier_not_found(self):
        test_query_id = "bad query identifier"
        sqlbuilder = SQLQueryBuilder(parsed_query_data={'q1': 'v1'})
        with self.assertRaises(SystemExit):
            sqlbuilder._raise_exception_if_query_identifier_not_found(query_id=test_query_id)

    def test_system_exit_when_parsed_query_data_is_empty(self):
        with self.assertRaises(SystemExit):
            SQLQueryBuilder(parsed_query_data={})


if __name__ == '__main__':
    unittest.main()
