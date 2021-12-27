######################################################
#
# Author: Davide Colombo
# Date: 20/12/21 19:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.sqltable import SQLTable, FilterSQLTable, JoinSQLTable
from airquality.sqlsearch import ILIKESearch

TEST_SELECTED_COLS = ["fake_col1", "fake_col2"]


class TestSQLTable(TestCase):

    @property
    def simple_sqltable(self):
        return SQLTable(table_name="fake_table", pkey="fake_pkey", selected_cols=TEST_SELECTED_COLS, schema="fake_schema", alias="fake_alias")

    @property
    def ilike_search(self):
        return ILIKESearch(search_column="fake_col1", search_value="v1", alias="fake_alias")

    @property
    def filter_sqltable(self):
        return FilterSQLTable(table_name="fake_table", pkey="fake_pkey", selected_cols=TEST_SELECTED_COLS,
                              schema="fake_schema", alias="fake_alias", search=self.ilike_search)

    def test_simple_sqltable(self):
        table = self.simple_sqltable
        self.assertEqual(table.join_cols, "fake_alias.fake_col1,fake_alias.fake_col2")
        self.assertEqual(table.select_key_condition(key="k1"), "WHERE fake_alias.fake_pkey=k1")
        self.assertEqual(table.delete_key_condition(key="k1"), "WHERE fake_alias.fake_pkey=k1")
        self.assertEqual(table.select_condition(), "")

    def test_filter_sqltable(self):
        table = self.filter_sqltable
        self.assertEqual(table.join_cols, "fake_alias.fake_col1,fake_alias.fake_col2")
        self.assertEqual(table.select_condition(), "WHERE fake_alias.fake_col1 ILIKE '%v1%'")
        self.assertEqual(table.select_key_condition(key="k1"), "WHERE fake_alias.fake_col1 ILIKE '%v1%' AND fake_alias.fake_pkey=k1")
        self.assertEqual(table.delete_key_condition(key="k1"), "WHERE fake_alias.fake_col1 ILIKE '%v1%' AND fake_alias.fake_pkey=k1")

    def test_join_sqltable_joined_to_simple_sqltable(self):
        join_table = self.simple_sqltable
        table = JoinSQLTable(table_name="fake_join", pkey="join_pkey", fkey="join_fkey", selected_cols=TEST_SELECTED_COLS,
                             schema="fake_schema", alias="join_alias", join_table=join_table)
        self.assertEqual(table.join_cols, "join_alias.fake_col1,join_alias.fake_col2")
        expected_join_cond = "INNER JOIN fake_schema.fake_table AS fake_alias ON join_alias.join_fkey=fake_alias.fake_pkey"
        self.assertEqual(table.join_cond, expected_join_cond)

        self.assertEqual(table.select_condition(), expected_join_cond + " ")

        self.assertEqual(table.select_key_condition(key="k1"), expected_join_cond + "  AND join_alias.join_pkey=k1")
        self.assertEqual(table.delete_key_condition(key="k1"), "WHERE join_alias.join_pkey=k1")

    def test_join_sqltable_joined_to_filter_sqltable(self):
        join_table = self.filter_sqltable
        table = JoinSQLTable(table_name="fake_join", pkey="join_pkey", fkey="join_fkey",
                             selected_cols=TEST_SELECTED_COLS,
                             schema="fake_schema", alias="join_alias", join_table=join_table)
        self.assertEqual(table.join_cols, "join_alias.fake_col1,join_alias.fake_col2")
        expected_join_cond = "INNER JOIN fake_schema.fake_table AS fake_alias ON join_alias.join_fkey=fake_alias.fake_pkey"
        self.assertEqual(table.join_cond, expected_join_cond)

        expected_filter_condition = " WHERE fake_alias.fake_col1 ILIKE '%v1%'"
        self.assertEqual(table.select_condition(), expected_join_cond + expected_filter_condition)

        self.assertEqual(table.select_key_condition(key="k1"), expected_join_cond + expected_filter_condition + " AND join_alias.join_pkey=k1")
        self.assertEqual(table.delete_key_condition(key="k1"), "WHERE join_alias.join_pkey=k1")


if __name__ == '__main__':
    main()
