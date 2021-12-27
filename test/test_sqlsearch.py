######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 11:27
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.sqlsearch import INSearch, EqualSearch, ILIKESearch


class TestSQLSearch(TestCase):

    def test_search_in(self):
        search = INSearch(search_column="c", search_value="v1,v2,v66", alias="a")
        self.assertEqual(search.search_condition(), "a.c IN ('v1','v2','v66')")
        print(repr(search))

    def test_search_in_with_one_value(self):
        search = INSearch(search_column="c", search_value="v2", alias="t")
        self.assertEqual(search.search_condition(), "t.c IN ('v2')")

    def test_equal_search(self):
        search = EqualSearch(search_column="c", search_value="v1", alias="s")
        self.assertEqual(search.search_condition(), "s.c = 'v1'")
        print(repr(search))

    def test_ilike_search(self):
        search = ILIKESearch(search_column="some_column", search_value="some_value")
        self.assertEqual(search.search_condition(), "t.some_column ILIKE '%some_value%'")
        print(repr(search))


if __name__ == '__main__':
    main()
