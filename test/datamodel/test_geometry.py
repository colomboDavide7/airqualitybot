######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 19:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.datamodel.geometry import PostgisPoint, NullGeometry


class TestGeometry(TestCase):

    def test_point_geometry(self):
        geo = PostgisPoint(latitude=5, longitude=10)
        self.assertEqual(geo.as_text(), "POINT(10 5)")
        self.assertEqual(geo.geom_from_text(), "ST_GeomFromText('POINT(10 5)', 26918)")

    def test_null_geometry(self):
        geo = NullGeometry()
        self.assertEqual(geo.as_text(), "NULL")
        self.assertEqual(geo.geom_from_text(), "NULL")

    def test_raise_ValueError_when_create_point_geometry(self):
        with self.assertRaises(ValueError):
            PostgisPoint(latitude=-92, longitude=147)

        with self.assertRaises(ValueError):
            PostgisPoint(latitude=97, longitude=-120)

        with self.assertRaises(ValueError):
            PostgisPoint(latitude=45, longitude=-190)

        with self.assertRaises(ValueError):
            PostgisPoint(latitude=-78, longitude=187)


if __name__ == '__main__':
    main()
