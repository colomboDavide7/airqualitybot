# ======================================
# @author:  Davide Colombo
# @date:    2022-01-24, lun, 08:30
# ======================================
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.requests import AddMobileMeasureRequest
from airquality.iterables.request_validator import AddSensorMeasuresRequestValidator


def _test_sensor_location():
    return PostgisPoint(
        latitude=11,
        longitude=-9
    )


def _test_sensor_measures():
    return [
        (66, 0.17),
        (48, 8),
        (94, 10),
        (2, 11),
        (4, 29),
        (12, 42),
        (39, 1004.68)
    ]


def _test_requests_timestamps():
    return [
        datetime.strptime("2021-08-10T23:59:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z"),
        datetime.strptime("2021-08-11T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
    ]


def _test_requests():
    return [
        AddMobileMeasureRequest(
            measures=_test_sensor_measures(),
            timestamp=ts,
            geolocation=_test_sensor_location()
        ) for ts in _test_requests_timestamps()
    ]


def _mocked_request_builder():
    mocked_rb = MagicMock()
    mocked_rb.__len__.return_value = len(_test_requests_timestamps())
    mocked_rb.__iter__.return_value = _test_requests()
    return mocked_rb


def _test_filter_timestamp():
    return datetime.strptime("2021-08-10T23:59:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")


class TestAddSensorMeasuresRequestValidator(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._validator = AddSensorMeasuresRequestValidator(
            request=_mocked_request_builder(),
            filter_ts=_test_filter_timestamp()
        )

# =========== TEST METHODS
    def test_validate_add_mobile_measure_request(self):
        self.assertEqual(
            len(self._validator),
            1
        )
        self._assert_valid_requests()

# =========== SUPPORT METHODS
    def _assert_valid_requests(self):
        req = self._validator[0]
        self.assertEqual(
            req.timestamp,
            datetime.strptime("2021-08-11T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        )


if __name__ == '__main__':
    main()
