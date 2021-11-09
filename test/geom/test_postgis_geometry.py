######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 20:37
# Description: unit test script
#
######################################################

import unittest
from airquality.geom.postgis_geometry import PostGISPoint


class TestPostgisGeometry(unittest.TestCase):

    def test_successfully_get_database_string_from_postgis_point(self):
        test_packet = {'lat': '45.1234', 'lng': '9.8765'}
        expected_output = f"ST_GeomFromText('POINT(9.8765 45.1234)', 26918)"
        point = PostGISPoint()
        actual_output = point.get_database_string(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_successfully_get_geomtype_from_postgis_point(self):
        test_packet = {'lat': '45.1234', 'lng': '9.8765'}
        expected_output = f"POINT(9.8765 45.1234)"
        point = PostGISPoint()
        actual_output = point.get_geomtype_string(test_packet)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
