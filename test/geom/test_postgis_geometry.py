######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 20:37
# Description: unit test script
#
######################################################

import unittest
from airquality.geom.postgis_geometry import PostGISPoint, PostGISNullObject


class TestPostgisGeometry(unittest.TestCase):

    def setUp(self) -> None:
        self.null_obj = PostGISNullObject()

    def test_successfully_get_database_string_from_postgis_point(self):
        expected_output = f"ST_GeomFromText('POINT(9.8765 45.1234)', 26918)"
        point = PostGISPoint(lat='45.1234', lng='9.8765')
        actual_output = point.get_database_string()
        self.assertEqual(actual_output, expected_output)

    def test_successfully_get_geomtype_from_postgis_point(self):
        expected_output = f"POINT(9.8765 45.1234)"
        point = PostGISPoint(lat='45.1234', lng='9.8765')
        actual_output = point.get_geomtype_string()
        self.assertEqual(actual_output, expected_output)

    def test_postgis_null_object(self):
        expected_output = 'null'
        actual_output = self.null_obj.get_database_string()
        self.assertEqual(actual_output, expected_output)

        actual_output = self.null_obj.get_geomtype_string()
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
