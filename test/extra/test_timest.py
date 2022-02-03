# ======================================
# @author:  Davide Colombo
# @date:    2022-01-19, mer, 14:27
# ======================================
from dateutil import tz
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import patch, MagicMock
import airquality.extra.timest as timest
import test._test_utils as tutils


def _new_york_timezone():
    return tutils.get_tzinfo_from_timezone_name('America/New_York')


def _rome_timezone():
    return tutils.get_tzinfo_from_timezone_name(tzname='Europe/Rome')


def _mocked_datetime() -> MagicMock:
    mocked_dt = MagicMock()
    mocked_dt.now.return_value = datetime(2022, 1, 23, 18, tzinfo=_rome_timezone())
    mocked_dt.astimezone.return_value = datetime(2022, 1, 23, 17, tzinfo=tz.tzutc())
    mocked_dt.replace.return_value = datetime(2022, 1, 23, 17, tzinfo=None)
    return mocked_dt


class TestTimestUtilityFunctions(TestCase):
    """
    A class for testing the timestamp conversion with or without fixed timezone, with or without an input/output format.
    """

    def test_make_naive_datetime(self):
        self.assertEqual(
            timest.make_naive(datetime(2021, 11, 11, 14, 35, tzinfo=_new_york_timezone())),
            datetime(2021, 11, 11, 19, 35, tzinfo=None)
        )

    def test_make_naive_current_timestamp(self):
        self.assertEqual(
            timest.make_naive(_mocked_datetime().now()),
            datetime(2022, 1, 23, 17, tzinfo=None)
        )

    def test_onthefly_convert_utc_time_without_timezone_to_utc_time_with_timezone_from_timezone_name(self):
        test_timezone_name = 'Europe/Rome'
        test_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
        expected_tzinfo = tutils.get_tzinfo_from_timezone_name(test_timezone_name)
        self.assertEqual(
            timest.make_timezone_aware_FROM_NAME(utctime='2021-08-08T00:00:00.000Z', timezone_name=test_timezone_name, fmt=test_fmt),
            datetime(2021, 8, 8, 2, tzinfo=expected_tzinfo)
        )

    def test_onthefly_convert_utc_timestamp_without_timezone_into_utc_time_with_timezone_from_timezone_name(self):
        test_timezone_name = "America/New_York"
        expected_tzinfo = tutils.get_tzinfo_from_timezone_name(test_timezone_name)
        self.assertEqual(
            timest.make_timezone_aware_FROM_NAME(utctime=1642859435, timezone_name=test_timezone_name),
            datetime(2022, 1, 22, 8, 50, 35, tzinfo=expected_tzinfo)
        )

    def test_convert_utc_datetime_string_without_timezone_to_utc_datetime_with_timezone_from_coords(self):
        test_lat = 45.1686197
        test_lng = 9.1561581
        test_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
        expected_tzinfo = tutils.get_tzinfo_from_coordinates(latitude=test_lat, longitude=test_lng)
        self.assertEqual(
            timest.make_timezone_aware_FROM_COORDS(utctime='2021-08-08T00:00:00.000Z', latitude=test_lat, longitude=test_lng, fmt=test_fmt),
            datetime(2021, 8, 8, 2, 0, 0, tzinfo=expected_tzinfo)
        )

        test_lat = 40.7127281
        test_lng = -74.0060152
        expected_tzinfo = tutils.get_tzinfo_from_coordinates(latitude=test_lat, longitude=test_lng)
        self.assertEqual(
            timest.make_timezone_aware_FROM_COORDS(utctime='2021-12-08T00:00:00.000Z', latitude=test_lat, longitude=test_lng, fmt=test_fmt),
            datetime(2021, 12, 7, 19, 0, 0, tzinfo=expected_tzinfo)
        )

    def test_convert_utc_timestamp_without_timezone_to_utc_timestamp_with_timezone(self):
        test_lat = 45.1686197
        test_lng = 9.1561581
        expected_tzinfo = tutils.get_tzinfo_from_coordinates(latitude=test_lat, longitude=test_lng)
        self.assertEqual(
            timest.make_timezone_aware_FROM_COORDS(utctime=1531432748, latitude=test_lat, longitude=test_lng),
            datetime(2018, 7, 12, 23, 59, 8, tzinfo=expected_tzinfo)
        )

    def test_raise_type_error_when_passing_string_time_instead_of_unix_timestamp(self):
        with self.assertRaises(TypeError):
            timest.make_timezone_aware_FROM_COORDS(utctime="2021-10-11 09:44:00", latitude=10, longitude=20)

    def test_raise_type_error_when_passing_unix_timestamp_instead_of_string_time(self):
        with self.assertRaises(TypeError):
            timest.make_timezone_aware_FROM_COORDS(utctime=1531432748, latitude=10, longitude=20, fmt="%Y-%m-%d")

    def test_raise_value_error_when_wrong_format_is_used(self):
        with self.assertRaises(ValueError):
            timest.make_timezone_aware_FROM_COORDS(utctime='31-12-2021', latitude=10, longitude=20, fmt="%Y-%m-%d")

    @patch('airquality.extra.timest.datetime')
    def test_get_current_utc_time_in_current_timezone(self, mocked_datetime):
        mocked_now = MagicMock()
        mocked_now.return_value = datetime(2022, 1, 19, 19, 30, tzinfo=tz.tzutc())
        mocked_now.astimezone.return_value = datetime(2022, 1, 19, 20, 30, tzinfo=tz.tzlocal())
        mocked_datetime.now = mocked_now
        self.assertEqual(
            timest.now_utctz(),
            datetime(2022, 1, 19, 20, 30, tzinfo=tz.tzlocal())
        )

    def test_convert_utc_time_without_time_zone_into_utc_time_with_time_zone(self):
        test_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.assertEqual(
            timest.make_timezone_aware_UTC(utctime='2021-12-08T00:00:00.000Z', fmt=test_fmt),
            datetime(2021, 12, 8, tzinfo=tz.tzutc())
        )


if __name__ == '__main__':
    main()
