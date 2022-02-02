# ======================================
# @author:  Davide Colombo
# @date:    2022-01-20, gio, 20:56
# ======================================
from datetime import datetime
from unittest import TestCase, main
from airquality.datamodel.requests import AddMobileMeasureRequest


def _acquisition_timestamp_test_data():
    return datetime.strptime("2021-12-20T11:18:40Z", "%Y-%m-%dT%H:%M:%SZ")


def _measures_test_data():
    return [(12, 20.50), (13, 35.53), (14, 37.43), (15, 55), (16, 60)]


class TestAddSensorMeasuresRequest(TestCase):

# =========== TEST METHODS
    def test_request_for_adding_station_measures(self):
        request = AddMobileMeasureRequest(
            timestamp=_acquisition_timestamp_test_data(),
            measures=_measures_test_data()
        )
        self.assertEqual(request.timestamp, datetime(2021, 12, 20, 11, 18, 40))
        self._assert_measures(request.measures)

# =========== SUPPORT METHODS
    def _assert_measures(self, measures):
        self._assert_measure_item(measures[0], 12, 20.50)
        self._assert_measure_item(measures[1], 13, 35.53)
        self._assert_measure_item(measures[2], 14, 37.43)
        self._assert_measure_item(measures[3], 15, 55)
        self._assert_measure_item(measures[4], 16, 60)

    def _assert_measure_item(self, measure, ident, value):
        self.assertEqual(measure[0], ident)
        self.assertEqual(measure[1], value)


if __name__ == '__main__':
    main()
