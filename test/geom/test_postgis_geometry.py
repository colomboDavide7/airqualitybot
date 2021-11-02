######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 20:37
# Description: unit test script
#
######################################################

import unittest
from airquality.geom.postgis_geometry import PostGISPointFactory


class TestPostgisGeometry(unittest.TestCase):

    def test_successfully_get_database_string_from_postgis_point(self):
        test_lat = "45.1234"
        test_lng = "9.8765"
        point = PostGISPointFactory(lat=test_lat, lng=test_lng).create_geometry()
        expected_output = f"ST_GeomFromText('POINT(9.8765 45.1234)')"
        actual_output = point.get_database_string()
        self.assertEqual(actual_output, expected_output)

    def test_successfully_get_geomtype_from_postgis_point(self):
        test_lat = "45.1234"
        test_lng = "9.8765"
        point = PostGISPointFactory(lat=test_lat, lng=test_lng).create_geometry()
        expected_output = f"POINT(9.8765 45.1234)"
        actual_output = point.get_geomtype_string()
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
