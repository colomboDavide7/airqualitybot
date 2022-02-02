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
        self.assertEqual(
            str(geo),
            "ST_GeomFromText('POINT(10 5)', 4326)"
        )

    def test_null_geometry(self):
        geo = NullGeometry()
        self.assertEqual(
            str(geo),
            "NULL"
        )

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
