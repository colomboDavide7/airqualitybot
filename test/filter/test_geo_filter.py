######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 17:47
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.geofilt as flt
import airquality.types.apiresp.inforesp as resp
import airquality.types.geolocation as geotype
import airquality.types.postgis as pgis


class TestGeoFilter(unittest.TestCase):

    def setUp(self) -> None:
        geolocation1 = geotype.Geolocation(timestamp=None, geometry=pgis.PostgisPoint(lat="45", lng="9"))
        geolocation2 = geotype.Geolocation(timestamp=None, geometry=pgis.PostgisPoint(lat="46", lng="8"))
        geolocation3 = geotype.Geolocation(timestamp=None, geometry=pgis.PostgisPoint(lat="45.5", lng="8.5"))

        self.test_responses = [
            resp.SensorInfoResponse(sensor_name="n1", sensor_type="t1", channels=[], geolocation=geolocation1),
            resp.SensorInfoResponse(sensor_name="n2", sensor_type="t1", channels=[], geolocation=geolocation2),
            resp.SensorInfoResponse(sensor_name="n3", sensor_type="t1", channels=[], geolocation=geolocation3)
        ]

    def test_empty_list_when_active_locations_are_the_same(self):
        test_active_locations = {"n1": "POINT(9 45)"}
        resp_filter = flt.GeoFilter()
        resp_filter.with_database_locations(test_active_locations)
        actual = resp_filter.filter(resp2filter=self.test_responses)
        self.assertEqual(len(actual), 0)

    def test_successfully_filter_responses(self):
        test_active_locations = {"n1": "POINT(10 44)"}
        resp_filter = flt.GeoFilter()
        resp_filter.with_database_locations(test_active_locations)
        actual = resp_filter.filter(resp2filter=self.test_responses)
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].sensor_name, "n1")

    def test_empty_list_when_no_active_locations_is_fetched(self):
        test_active_locations = {"n4": "POINT(10 44)"}

        resp_filter = flt.GeoFilter()
        resp_filter.with_database_locations(test_active_locations)
        actual = resp_filter.filter(resp2filter=self.test_responses)
        self.assertEqual(len(actual), 0)


if __name__ == '__main__':
    unittest.main()
