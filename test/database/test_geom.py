######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 20:37
# Description: unit test script
#
######################################################
import unittest
import airquality.database.util.postgis.geom as geom


class TestGeometryBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.point_builder = geom.PointBuilder(srid=26918)

    def test_successfully_get_database_string_from_postgis_point(self):
        test_packet = {'lat': '45.1234', 'lng': '9.8765'}
        expected_output = f"ST_GeomFromText('POINT(9.8765 45.1234)', 26918)"
        actual_output = self.point_builder.geom_from_text(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_successfully_get_geomtype_from_postgis_point(self):
        test_packet = {'lat': '45.1234', 'lng': '9.8765'}
        expected_output = f"POINT(9.8765 45.1234)"
        actual_output = self.point_builder.as_text(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_null_on_missing_geolocation(self):
        test_missing_lng = {'lat': '45.1234'}
        actual_output = self.point_builder._null_on_missing_geolocation(test_missing_lng)
        self.assertEqual(actual_output, "NULL")

        test_missing_lat = {'lng': '1.1234'}
        actual_output = self.point_builder._null_on_missing_geolocation(test_missing_lat)
        self.assertEqual(actual_output, "NULL")


if __name__ == '__main__':
    unittest.main()
