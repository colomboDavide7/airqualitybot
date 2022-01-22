# ======================================
# @author:  Davide Colombo
# @date:    2022-01-22, sab, 16:29
# ======================================
from datetime import datetime
import test._test_utils as tutils
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.timest import atmotube_timest
from airquality.datamodel.apidata import AtmotubeAPIData
from airquality.datamodel.geometry import PostgisPoint, NullGeometry
from airquality.core.request_builder import AddAtmotubeMeasureRequestBuilder


def _test_measure_param_map():
    return {'voc': 66, 'pm1': 48, 'pm25': 94, 'pm10': 2, 't': 4, 'h': 12, 'p': 39}


def _test_datamodel_without_coords():
    return AtmotubeAPIData(
        time="2021-08-11T00:00:00.000Z",
        voc=0.19,
        pm1=7,
        p=1007.03
    )


def _test_datamodel_with_coords():
    return AtmotubeAPIData(
        time="2021-08-10T23:59:00.000Z",
        voc=0.17,
        pm1=8,
        pm25=10,
        pm10=11,
        t=29,
        h=42,
        p=1004.68,
        coords={'lat': 45.765, 'lon': 9.897}
    )


def _mocked_datamodel_builder():
    mocked_db = MagicMock()
    mocked_db.__iter__.return_value = [
        _test_datamodel_with_coords(),
        _test_datamodel_without_coords()
    ]
    return mocked_db


def _expected_location_first_request():
    return PostgisPoint(latitude=45.765, longitude=9.897)


def _expected_measures_first_request():
    return [
        (66, 0.17),
        (48, 8),
        (94, 10),
        (2, 11),
        (4, 29),
        (12, 42),
        (39, 1004.68)
    ]


def _expected_timestamp_first_request():
    tzinf = tutils.get_tzinfo_from_coordinates(
        latitude=45.765,
        longitude=9.897
    )
    return datetime(2021, 8, 11, 1, 59, tzinfo=tzinf)


def _expected_measures_second_request():
    return [
        (66, 0.19),
        (48, 7),
        (39, 1007.03)
    ]


class TestAddAtmotubeMeasuresRequestBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._builder = AddAtmotubeMeasureRequestBuilder(
            datamodel=_mocked_datamodel_builder(),
            timest=atmotube_timest(),
            code2id=_test_measure_param_map()
        )

# =========== TEST METHODS
    def test_create_request_for_adding_atmotube_measure(self):
        self.assertEqual(
            len(self._builder),
            2
        )
        self._assert_first_request()
        self._assert_second_request()

# =========== SUPPORT METHODS
    def _assert_first_request(self):
        request = self._builder[0]
        self.assertEqual(
            request.timestamp,
            _expected_timestamp_first_request()
        )
        self.assertEqual(
            request.geolocation,
            _expected_location_first_request()
        )
        self.assertEqual(
            request.measures,
            _expected_measures_first_request()
        )

    def _assert_second_request(self):
        request = self._builder[1]
        self.assertEqual(
            request.timestamp,
            datetime(2021, 8, 11, tzinfo=tutils.get_utc_tz())
        )
        self.assertEqual(
            request.measures,
            _expected_measures_second_request()
        )
        self.assertIsInstance(
            request.geolocation,
            NullGeometry
        )


if __name__ == '__main__':
    main()
