# ======================================
# @author:  Davide Colombo
# @date:    2022-01-24, lun, 09:03
# ======================================
from datetime import datetime
import test._test_utils as tutils
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.request import AddMobileMeasuresRequest
from airquality.iterables.response_builder import AddMobileMeasureResponseBuilder


def _rome_timezone():
    return tutils.get_tzinfo_from_timezone_name(tzname='Europe/Rome')


def _test_acquisition_timestamp():
    return datetime(2021, 12, 29, 19, 33, tzinfo=_rome_timezone())


def _test_sensor_location():
    return PostgisPoint(
        latitude=45.876,
        longitude=9.145
    )


def _test_measures():
    return [
        (66, 0.17),
        (48, 8),
        (94, 10),
        (2, 11),
        (4, 29),
        (12, 42),
        (39, 1004.68)
    ]


def _test_requests():
    return AddMobileMeasuresRequest(
        timestamp=_test_acquisition_timestamp(),
        geolocation=_test_sensor_location(),
        measures=_test_measures()
    )


def _mocked_validator():
    mocked_v = MagicMock()
    mocked_v.__len__.return_value = 1
    mocked_v.__iter__.return_value = [_test_requests()]
    return mocked_v


def _expected_measure_record():
    geom = "ST_GeomFromText('POINT(9.145 45.876)', 4326)"
    ts = "2021-12-29 19:33:00+01:00"
    return f"(12399, 66, 0.17, '{ts}', {geom})," \
           f"(12399, 48, 8, '{ts}', {geom})," \
           f"(12399, 94, 10, '{ts}', {geom})," \
           f"(12399, 2, 11, '{ts}', {geom})," \
           f"(12399, 4, 29, '{ts}', {geom})," \
           f"(12399, 12, 42, '{ts}', {geom})," \
           f"(12399, 39, 1004.68, '{ts}', {geom})"


class TestAddAtmotubeMeasuresResponseBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._response_builder = AddMobileMeasureResponseBuilder(
            requests=_mocked_validator(),
            start_packet_id=12399
        )

# =========== TEST METHOD
    def test_create_response_to_request_of_adding_mobile_measure(self):
        self.assertEqual(
            self._response_builder[0].measure_record,
            _expected_measure_record()
        )


if __name__ == '__main__':
    main()
