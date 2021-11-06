######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 11:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

import unittest
from airquality.adapter.geom_adapter import GeometryAdapterPurpleair


class TestGeomAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.geom_adapter = GeometryAdapterPurpleair()

    def test_successfully_adapt_purpleair_packet(self):
        test_packet = {'latitude': 'l1', 'longitude': 'l2'}
        expected_output = {'lat': 'l1', 'lng': 'l2'}
        actual_output = self.geom_adapter.adapt_packet(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_purpleair_geometry_keys_are_missing(self):
        test_packet = {'latitude': 'l1'}
        with self.assertRaises(SystemExit):
            self.geom_adapter.adapt_packet(test_packet)

        test_packet = {'longitude': 'l1'}
        with self.assertRaises(SystemExit):
            self.geom_adapter.adapt_packet(test_packet)


if __name__ == '__main__':
    unittest.main()
