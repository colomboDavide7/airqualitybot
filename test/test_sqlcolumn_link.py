######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 15:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.sqlcolumn import MaxColumn, CountColumn, SQLColumn
from airquality.sqlcolumn_link import SQLColumnLink, DecoratedSQLColumnLink


class TestSQLColumnLink(TestCase):

    @property
    def max_column(self):
        return MaxColumn(target_column="id")

    @property
    def count_column(self):
        return CountColumn(target_column="packet")

    @property
    def plain_column(self):
        return SQLColumn(target_column="some_col")

    def test_link_columns(self):
        col = SQLColumnLink(columns=[self.max_column, self.count_column])
        self.assertEqual(col.selected_columns(), "MAX(t.id),COUNT(t.packet)")
        print(repr(col))

    def test_column_link_with_empty_values(self):
        with self.assertRaises(ValueError):
            SQLColumnLink(columns=[])

    def test_decorated_column_link(self):
        link = SQLColumnLink(columns=[self.max_column, self.count_column])
        decorated_link = DecoratedSQLColumnLink(columns=[self.plain_column], linked=link)
        self.assertEqual(decorated_link.selected_columns(), "MAX(t.id),COUNT(t.packet),t.some_col")

    def test_multi_decorated_column_link(self):
        link = SQLColumnLink(columns=[self.max_column, self.count_column])
        decorated_link = DecoratedSQLColumnLink(columns=[self.plain_column], linked=link)
        decorated_link2 = DecoratedSQLColumnLink(columns=[self.plain_column], linked=decorated_link)
        self.assertEqual(decorated_link2.selected_columns(), "MAX(t.id),COUNT(t.packet),t.some_col,t.some_col")
        print(repr(decorated_link2))


if __name__ == '__main__':
    main()
