# ======================================
# @author:  Davide Colombo
# @date:    2022-01-20, gio, 20:47
# ======================================
from datetime import datetime
from unittest import TestCase, main
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.requests import AddSensorMeasureRequest


def _acquisition_timestamp_test_data():
    return datetime.strptime("2021-10-11T09:44:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")


def _measures_test_data():
    return [(1, 0.17), (2, 24), (3, 32)]


def _location_test_data():
    return PostgisPoint(latitude=44.98, longitude=-9.23)


def _expected_geom_from_text():
    return "ST_GeomFromText('POINT(-9.23 44.98)', 4326)"


class TestAddAtmotubeMeasureRequest(TestCase):

# =========== TEST METHODS
    def test_request_for_adding_mobile_sensor_measure(self):
        request = AddSensorMeasureRequest(
            timestamp=_acquisition_timestamp_test_data(),
            geolocation=_location_test_data(),
            measures=_measures_test_data()
        )
        self.assertEqual(request.timestamp, datetime(2021, 10, 11, 9, 44))
        self.assertEqual(str(request.geolocation), _expected_geom_from_text())
        self._assert_measures(request.measures)

# =========== SUPPORT METHODS
    def _assert_measures(self, measures):
        self._assert_measure_item(measures[0], 1, 0.17)
        self._assert_measure_item(measures[1], 2, 24)
        self._assert_measure_item(measures[2], 3, 32)

    def _assert_measure_item(self, measure, ident, value):
        self.assertEqual(measure[0], ident)
        self.assertEqual(measure[1], value)


if __name__ == '__main__':
    main()
