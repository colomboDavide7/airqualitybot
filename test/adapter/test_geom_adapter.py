######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 11:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

import unittest
from airquality.adapter.geom_adapter import GeometryAdapterPurpleair, GeometryAdapterAtmotube, PostGISPoint, \
    PostGISNullObject


class TestGeomAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.purpleair_adapter = GeometryAdapterPurpleair()
        self.atmotube_adapter = GeometryAdapterAtmotube()

    def test_successfully_adapt_purpleair_packet(self):
        test_packet = {'lat': 'l1', 'lng': 'l2'}
        expected_output = PostGISPoint(lat='l1', lng='l2')
        actual_output = self.purpleair_adapter.adapt(test_packet)
        self.assertEqual(actual_output, expected_output)

    ############################## TEST ATMOTUBE GEOMETRY ADAPTER #############################
    def test_successfully_adapt_atmotube_packet(self):
        test_packet = {'coords': {'lat': 'l1', 'lon': 'l2'}}
        expected_output = PostGISPoint(lat='l1', lng='l2')
        actual_output = self.atmotube_adapter.adapt(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_postgis_null_object_when_coords_is_missing(self):
        test_packet = {}
        expected_output = PostGISNullObject()
        actual_output = self.atmotube_adapter.adapt(test_packet)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
