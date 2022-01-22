# ======================================
# @author:  Davide Colombo
# @date:    2022-01-19, mer, 14:27
# ======================================
from dateutil import tz
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import patch, MagicMock
from airquality.datamodel.timest import Timest, TimestConversionError
import test._test_utils as tutils


class TestTimest(TestCase):
    """
    A class for testing the timestamp conversion with or without fixed timezone, with or without an input/output format.
    """

# =========== TEST _RotatingTimezone using time zone name
    def test_onthefly_convert_utc_time_without_timezone_to_utc_time_with_timezone_from_timezone_name(self):
        test_timezone_name = 'Europe/Rome'
        timest = Timest(input_fmt="%Y-%m-%dT%H:%M:%S.%fZ")
        expected_tzinfo = tutils.get_tzinfo_from_timezone_name(test_timezone_name)
        self.assertEqual(
            timest.utc_time2utc_localtz(time='2021-08-08T00:00:00.000Z', tzname=test_timezone_name),
            datetime(2021, 8, 8, 2, tzinfo=expected_tzinfo)
        )

    def test_onthefly_convert_utc_timestamp_without_timezone_into_utc_time_with_timezone_from_timezone_name(self):
        test_timezone_name = "America/New_York"
        timest = Timest()
        expected_tzinfo = tutils.get_tzinfo_from_timezone_name(test_timezone_name)
        self.assertEqual(
            timest.utc_time2utc_localtz(time=1642859435, tzname=test_timezone_name),
            datetime(2022, 1, 22, 8, 50, 35, tzinfo=expected_tzinfo)
        )

    def test_raise_time_conversion_error_when_onthefly_convert_timestamp_without_specifying_timezone_name(self):
        timest = Timest()
        with self.assertRaises(TimestConversionError):
            timest.utc_time2utc_localtz(time=1642859435)

# =========== TEST _RotatingTimezone using time zone latitude and longitude
    def test_convert_utc_datetime_string_without_timezone_to_utc_datetime_with_timezone(self):
        # Pavia's timestamp with timezone IN DST is +2 hours, NOT IN DST is +1 hour
        test_lat = 45.1686197
        test_lng = 9.1561581
        timest = Timest(input_fmt="%Y-%m-%dT%H:%M:%S.%fZ")
        expected_tzinfo = tutils.get_tzinfo_from_coordinates(latitude=test_lat, longitude=test_lng)
        self.assertEqual(
            timest.utc_time2utc_localtz(time='2021-08-08T00:00:00.000Z', latitude=test_lat, longitude=test_lng),
            datetime(2021, 8, 8, 2, 0, 0, tzinfo=expected_tzinfo)
        )

        # New York's timestamp with timezone NOT IN DST is -5 hours, IN DST is -4 hours
        test_lat = 40.7127281
        test_lng = -74.0060152
        timest = Timest(input_fmt="%Y-%m-%dT%H:%M:%S.%fZ")
        expected_tzinfo = tutils.get_tzinfo_from_coordinates(latitude=test_lat, longitude=test_lng)
        self.assertEqual(
            timest.utc_time2utc_localtz(time='2021-12-08T00:00:00.000Z', latitude=test_lat, longitude=test_lng),
            datetime(2021, 12, 7, 19, 0, 0, tzinfo=expected_tzinfo)
        )

    def test_convert_utc_timestamp_without_timezone_to_utc_timestamp_with_timezone(self):
        test_lat = 45.1686197
        test_lng = 9.1561581
        timest = Timest()
        expected_tzinfo = tutils.get_tzinfo_from_coordinates(latitude=test_lat, longitude=test_lng)
        self.assertEqual(
            timest.utc_time2utc_localtz(time=1531432748, latitude=test_lat, longitude=test_lng),
            datetime(2018, 7, 12, 23, 59, 8, tzinfo=expected_tzinfo)
        )

    def test_raise_timest_conversion_error_when_passing_string_time_instead_of_unix_timestamp(self):
        timest = Timest()
        with self.assertRaises(TimestConversionError):
            timest.utc_time2utc_localtz(time="2021-10-11 09:44:00", latitude=10, longitude=20)

    def test_raise_timest_conversion_error_when_passing_unix_timestamp_instead_of_string_time(self):
        timest = Timest(input_fmt="%Y-%m-%d")
        with self.assertRaises(TimestConversionError):
            timest.utc_time2utc_localtz(time=1531432748, latitude=10, longitude=20)

    def test_raise_timest_conversion_error_when_wrong_format_is_used(self):
        timest = Timest(input_fmt="%Y-%m-%d")
        with self.assertRaises(TimestConversionError):
            timest.utc_time2utc_localtz(time='31-12-2021', latitude=10, longitude=20)

    @patch('airquality.datamodel.timest.datetime')
    def test_get_current_utc_time_in_current_timezone(self, mocked_datetime):
        mocked_now = MagicMock()
        mocked_now.return_value = datetime(2022, 1, 19, 19, 30, tzinfo=tz.tzutc())
        mocked_now.astimezone.return_value = datetime(2022, 1, 19, 20, 30, tzinfo=tz.tzlocal())
        mocked_datetime.now = mocked_now
        self.assertEqual(
            Timest.current_utc_timetz(),
            datetime(2022, 1, 19, 20, 30, tzinfo=tz.tzlocal())
        )

    def test_convert_utc_time_without_time_zone_into_utc_time_with_time_zone(self):
        timest = Timest(input_fmt="%Y-%m-%dT%H:%M:%S.%fZ")
        self.assertEqual(
            timest.utc_time2utc_tz(time='2021-12-08T00:00:00.000Z'),
            datetime(2021, 12, 8, tzinfo=tz.tzutc())
        )

    def test_raise_time_conversion_error_when_converting_time_without_specify_geolocation(self):
        timest = Timest()
        with self.assertRaises(TimestConversionError):
            timest.utc_time2utc_localtz(time=1531432748)

# =========== TEST _FixedTimezone
    def test_convert_utc_time_without_time_zone_into_utc_time_with_fixed_time_zone(self):
        timest = Timest(latitude=45, longitude=9)
        expected_tzinfo = tutils.get_tzinfo_from_coordinates(latitude=45, longitude=9)
        self.assertEqual(
            timest.utc_time2utc_localtz(time=1531432748),
            datetime(2018, 7, 12, 23, 59, 8, tzinfo=expected_tzinfo)
        )

    def test_raise_timest_conversion_error_when_try_to_use_a_different_location_with_fixed_timezone(self):
        timest = Timest(latitude=45, longitude=9)
        with self.assertRaises(TimestConversionError):
            timest.utc_time2utc_localtz(time=1531432748, longitude=10, latitude=44)

# =========== TEST _FixedTimezoneWithName
    def test_convert_utc_time_without_time_zone_into_utc_time_with_fixed_time_zone_from_name(self):
        test_timezone_name = "America/New_York"
        timest = Timest(tz_name=test_timezone_name)
        expected_tzinfo = tutils.get_tzinfo_from_timezone_name(test_timezone_name)
        self.assertEqual(
            timest.utc_time2utc_localtz(time=1642859435),
            datetime(2022, 1, 22, 8, 50, 35, tzinfo=expected_tzinfo)
        )

    def test_raise_timest_conversion_error_when_using_location_arguments_with_fixed_timezone_maker_with_name(self):
        timest = Timest(tz_name="Europe/Rome")
        with self.assertRaises(TimestConversionError):
            timest.utc_time2utc_localtz(time=1642859435, latitude=45, longitude=9)


if __name__ == '__main__':
    main()
