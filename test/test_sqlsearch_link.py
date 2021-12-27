######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 11:42
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.sqlsearch_link import DecoratedSQLSearchLink, SQLSearchLink
from airquality.sqlsearch import INSearch, EqualSearch, ILIKESearch


class TestSQLLink(TestCase):

    @property
    def ilike_search(self):
        return ILIKESearch(search_column="c4", search_value="us", alias="p")

    @property
    def in_search(self):
        return INSearch(search_column="c1", search_value="v1,v2", alias="a")

    @property
    def equal_search(self):
        return EqualSearch(search_column="c2", search_value="v13", alias="e")

    @property
    def search_conditions(self):
        return [self.in_search, self.equal_search]

    def test_ValueError_when_less_than_two_conditions_are_passed(self):
        with self.assertRaises(ValueError):
            SQLSearchLink(search_conditions=[], link_keyword="AND", min_len=2)

    def test_and_link(self):
        link = SQLSearchLink(search_conditions=self.search_conditions, link_keyword="AND", min_len=2)
        expected = "a.c1 IN ('v1','v2') AND e.c2 = 'v13'"
        self.assertEqual(link.search_condition(), expected)
        print(repr(link))

    def test_link_one_condition(self):
        with self.assertRaises(ValueError):
            SQLSearchLink(search_conditions=[self.equal_search], link_keyword="AND")

    def test_decorated_link(self):
        link = SQLSearchLink(search_conditions=self.search_conditions, link_keyword="AND", min_len=2)
        link2 = DecoratedSQLSearchLink(linked=link, search_conditions=[self.ilike_search], link_keyword="OR")
        expected = "a.c1 IN ('v1','v2') AND e.c2 = 'v13' OR p.c4 ILIKE '%us%'"
        self.assertEqual(link2.search_condition(), expected)
        print(repr(link2))

    def test_multiple_decorated_linked_search(self):
        link = SQLSearchLink(search_conditions=self.search_conditions, link_keyword="OR", min_len=2)
        decorated_link = DecoratedSQLSearchLink(search_conditions=[self.in_search], link_keyword="AND", linked=link)
        decorated_link_2 = DecoratedSQLSearchLink(search_conditions=[self.ilike_search], link_keyword="AND", linked=decorated_link)
        expected = "a.c1 IN ('v1','v2') OR e.c2 = 'v13' AND a.c1 IN ('v1','v2') AND p.c4 ILIKE '%us%'"
        self.assertEqual(decorated_link_2.search_condition(), expected)
        print(repr(decorated_link_2))


if __name__ == '__main__':
    main()
