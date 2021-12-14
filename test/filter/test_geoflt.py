######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 17:47
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.geoflt as flt
import airquality.api.resp.purpleair as resptype


class TestGeoFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.test_responses = [
            resptype.PurpleairAPIRespType(item={'name': 'n1', 'sensor_index': 'idx1', 'latitude': '45', 'longitude': '9'}),
            resptype.PurpleairAPIRespType(item={'name': 'n2', 'sensor_index': 'idx2', 'latitude': '46', 'longitude': '8'}),
            resptype.PurpleairAPIRespType(item={'name': 'n3', 'sensor_index': 'idx3', 'latitude': '45.5', 'longitude': '8.5'})
        ]

    def test_output_empty_list_when_active_locations_are_unchanged(self):
        test_database_locations = {'n1 (idx1)': 'POINT(9 45)'}
        resp_filter = flt.GeolocationFilter(name2geom_as_text=test_database_locations)
        actual = resp_filter.filter(self.test_responses)
        self.assertEqual(len(actual), 0)

    def test_successfully_filter_responses(self):
        test_database_locations = {'n1 (idx1)': 'POINT(10 44)'}
        resp_filter = flt.GeolocationFilter(name2geom_as_text=test_database_locations)
        actual = resp_filter.filter(self.test_responses)
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].sensor_name(), "n1 (idx1)")

    def test_output_empty_list_when_locations_are_inactive(self):
        test_database_locations = {'n4 (idx4)': 'POINT(-9 34)'}
        resp_filter = flt.GeolocationFilter(name2geom_as_text=test_database_locations)
        actual = resp_filter.filter(self.test_responses)
        self.assertEqual(len(actual), 0)


if __name__ == '__main__':
    unittest.main()
