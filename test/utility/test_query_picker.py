#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:32
# @Description: unit test script
#
#################################################
import unittest
from utility.query_picker import QueryPicker


class TestSQLQueryBuilder(unittest.TestCase):

    def test_system_exit_when_query_identifier_not_found(self):
        test_query_id = "bad query identifier"
        sqlbuilder = QueryPicker(parsed_query_data={'q1': 'v1'})
        with self.assertRaises(SystemExit):
            sqlbuilder.search_query_id(query_id=test_query_id)


if __name__ == '__main__':
    unittest.main()
