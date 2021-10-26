#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 19:15
# @Description: unit test script
#
#################################################


import unittest
from airquality.geom.postgis_geom_builder import PostGISGeomBuilder
from airquality.constants.shared_constants import EMPTY_STRING, EMPTY_DICT, \
    GEO_TYPE_ST_POINT_2D, GEOMBUILDER_LATITUDE, GEOMBUILDER_LONGITUDE


class TestPostGISGeomBuilder(unittest.TestCase):


    def test_empty_string_when_passing_empty_geo_param(self):
        """Test 'EMPTY_STRING' output value when 'EMPTY_DICT' is passed."""

        actual_output = PostGISGeomBuilder.build_geometry_type(geo_param = EMPTY_DICT, geo_type = GEO_TYPE_ST_POINT_2D)
        self.assertEqual(actual_output, EMPTY_STRING)


    def test_system_exit_when_missing_param(self):
        """Test SystemExit when some parameter is missing from 'geo_param' argument."""

        test_param = {GEOMBUILDER_LATITUDE: "45.676289"}
        with self.assertRaises(SystemExit):
            PostGISGeomBuilder.build_geometry_type(geo_param = test_param, geo_type = GEO_TYPE_ST_POINT_2D)


    def test_system_exit_when_bad_geotype_is_requested(self):
        """Test SystemExit when bad geometry type is passed."""

        test_param = {GEOMBUILDER_LATITUDE: "45.676289", GEOMBUILDER_LONGITUDE: "9.6473648"}
        with self.assertRaises(SystemExit):
            PostGISGeomBuilder.build_geometry_type(geo_param = test_param, geo_type = "bad geometry type")



if __name__ == '__main__':
    unittest.main()
