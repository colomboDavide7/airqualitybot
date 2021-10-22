#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 19:15
# @Description: unit test script
#
#################################################


import unittest
from airquality.geom.postgis_geom_builder import PostGISGeomBuilder


class TestPostGISGeomBuilder(unittest.TestCase):


    def test_point_from_coords(self):
        x = 1.234
        y = 6.543

        expected_output = f"ST_GeomFromText('POINT({x} {y})', {PostGISGeomBuilder.EPSG_SRID})"
        actual_output = PostGISGeomBuilder.build_ST_Point_from_coords(x, y)
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()
