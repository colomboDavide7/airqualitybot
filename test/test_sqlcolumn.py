######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 15:45
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.sqlcolumn import SQLColumn, MaxColumn, CountColumn, ST_X_Column, ST_Y_Column


class TestSQLColumn(TestCase):

    def test_max_column(self):
        col = MaxColumn(target_column="c1")
        self.assertEqual(col.selected_columns(), "MAX(t.c1)")

    def test_count_column(self):
        col = CountColumn(target_column="c66", alias="r")
        self.assertEqual(col.selected_columns(), "COUNT(r.c66)")

    def test_base_column(self):
        col = SQLColumn(target_column="some_col", alias="some_alias")
        self.assertEqual(col.selected_columns(), "some_alias.some_col")

    def test_postgis_latitude_function(self):
        col = ST_Y_Column(target_column="geom", alias="g")
        self.assertEqual(col.selected_columns(), "ST_Y(g.geom)")

    def test_postgis_longitude_function(self):
        col = ST_X_Column(target_column="geom", alias="g")
        self.assertEqual(col.selected_columns(), "ST_X(g.geom)")


if __name__ == '__main__':
    main()
