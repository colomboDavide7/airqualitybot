#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:32
# @Description: unit test script
#
#################################################
import unittest
import airquality.utility.picker.query as pk


class TestSQLQueryBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.picker = pk.QueryPicker({'q1': 'v1'})

    def test_system_exit_when_query_identifier_not_found(self):
        with self.assertRaises(SystemExit):
            self.picker.search_query_id("bad query identifier")


if __name__ == '__main__':
    unittest.main()
