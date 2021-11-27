######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 20:37
# Description: unit test script
#
######################################################
import unittest
import airquality.types.postgis as geom


class TestGeometryBuilder(unittest.TestCase):

    def test_successfully_get_database_string_from_postgis_point(self):
        expected_output = f"ST_GeomFromText('POINT(9.8765 45.1234)', 26918)"
        actual_output = geom.PostgisPoint(lat='45.1234', lng='9.8765').geom_from_text()
        self.assertEqual(actual_output, expected_output)

    def test_successfully_get_geomtype_from_postgis_point(self):
        expected_output = f"POINT(9.8765 45.1234)"
        actual_output = geom.PostgisPoint(lat='45.1234', lng='9.8765').as_text()
        self.assertEqual(actual_output, expected_output)

    def test_null_object_geom_from_text(self):
        expected_output = "NULL"
        actual_output = geom.NullGeometry().geom_from_text()
        self.assertEqual(actual_output, expected_output)

    def test_null_object_as_text(self):
        expected_output = "NULL"
        actual_output = geom.NullGeometry().as_text()
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
