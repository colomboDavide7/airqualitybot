#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 19:15
# @Description: unit test script
#
#################################################


import unittest
from airquality.app import EMPTY_STRING
from airquality.geom import GEO_TYPE_ST_POINT_2D
from airquality.geom.postgis_geom_builder import PosGISGeomBuilderFactory


class TestPostGISGeomBuilder(unittest.TestCase):


    def setUp(self) -> None:
        self.factory = PosGISGeomBuilderFactory()


    def test_empty_string_when_passing_empty_geo_param_build_purpleair_geo_type(self):

        geo_builder = self.factory.create_posGISGeomBuilder(bot_personality = "purpleair")
        actual_output = geo_builder.build_geometry_type(geo_param = {}, geo_type = GEO_TYPE_ST_POINT_2D)
        self.assertEqual(actual_output, EMPTY_STRING)


    def test_missing_param_purpleair_geo_type(self):

        test_param = {"latitude": "45.676289"}
        geo_builder = self.factory.create_posGISGeomBuilder(bot_personality = "purpleair")
        with self.assertRaises(SystemExit):
            geo_builder.build_geometry_type(geo_param = test_param, geo_type = GEO_TYPE_ST_POINT_2D)


    def test_system_exit_when_bad_geotype_purpleair_geometry(self):

        test_param = {"latitude": "45.676289", "longitude": "9.6473648"}
        geo_builder = self.factory.create_posGISGeomBuilder(bot_personality = "purpleair")
        with self.assertRaises(SystemExit):
            geo_builder.build_geometry_type(geo_param = test_param, geo_type = "bad geometry type")



if __name__ == '__main__':
    unittest.main()
