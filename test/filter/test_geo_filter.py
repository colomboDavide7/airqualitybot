######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 17:47
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
from typing import Generator
import airquality.filter.geolocation as flt
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

    def generate_responses(self) -> Generator[resp.SensorInfoResponse, None, None]:
        for response in self.test_responses:
            yield response

    def test_empty_list_when_active_locations_are_the_same(self):
        resp_filter = flt.GeoFilter()
        resp_filter.with_database_locations({"n1": pgis.PostgisPoint(lat="45", lng="9").as_text()})
        actual = resp_filter.filter(self.test_responses)
        self.assertEqual(len(actual), 0)

    def test_successfully_filter_responses(self):
        resp_filter = flt.GeoFilter()
        resp_filter.with_database_locations({"n1": pgis.PostgisPoint(lat="44", lng="10").as_text()})
        actual = resp_filter.filter(self.test_responses)
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].sensor_name, "n1")

    def test_empty_list_when_no_active_locations_is_fetched(self):
        resp_filter = flt.GeoFilter()
        actual = resp_filter.filter(self.test_responses)
        self.assertEqual(len(actual), 0)


if __name__ == '__main__':
    unittest.main()
