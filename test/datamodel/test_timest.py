# ======================================
# @author:  Davide Colombo
# @date:    2022-01-19, mer, 14:27
# ======================================
from dateutil import tz
from datetime import datetime
from unittest import TestCase, main
from timezonefinder import TimezoneFinder
from airquality.datamodel.timest import Timest, TimestConversionError


class TestTimest(TestCase):

    @property
    def tz_finder(self):
        return TimezoneFinder()

    def get_test_timezone_info(self, lat: float, lng: float):
        return tz.gettz(self.tz_finder.timezone_at(lat=lat, lng=lng))

    def test_convert_utc_datetime_string_without_timezone_to_utc_datetime_with_timezone(self):
        # Pavia's timestamp with timezone IN DST is +2 hours, NOT IN DST is +1 hour
        test_lat = 45.1686197
        test_lng = 9.1561581
        timest = Timest(input_fmt="%Y-%m-%dT%H:%M:%S.%fZ")
        actual = timest.utc_time2utc_timetz(time='2021-08-08T00:00:00.000Z', latitude=test_lat, longitude=test_lng)
        expected_tzinfo = self.get_test_timezone_info(lat=test_lat, lng=test_lng)
        self.assertEqual(actual, datetime(2021, 8, 8, 0, 0, 0, tzinfo=expected_tzinfo))

        # New York's timestamp with timezone NOT IN DST is -5 hours, IN DST is -4 hours
        test_lat = 40.7127281
        test_lng = -74.0060152
        timest = Timest(input_fmt="%Y-%m-%dT%H:%M:%S.%fZ")
        actual = timest.utc_time2utc_timetz(time='2021-12-08T00:00:00.000Z', latitude=test_lat, longitude=test_lng)
        expected_tzinfo = self.get_test_timezone_info(lat=test_lat, lng=test_lng)
        self.assertEqual(actual, datetime(2021, 12, 8, 0, 0, 0, tzinfo=expected_tzinfo))

    def test_convert_utc_timestamp_without_timezone_to_utc_timestamp_with_timezone(self):
        test_lat = 45.1686197
        test_lng = 9.1561581
        timest = Timest()
        actual = timest.utc_time2utc_timetz(time=1531432748, latitude=test_lat, longitude=test_lng)
        expected_tzinfo = self.get_test_timezone_info(lat=test_lat, lng=test_lng)
        self.assertEqual(actual, datetime(2018, 7, 12, 21, 59, 8, tzinfo=expected_tzinfo))

    def test_raise_timest_conversion_error_when_passing_string_time_instead_of_unix_timestamp(self):
        timest = Timest()
        with self.assertRaises(TimestConversionError):
            timest.utc_time2utc_timetz(time="2021-10-11 09:44:00", latitude=10, longitude=20)

    def test_raise_timest_conversion_error_when_passing_unix_timestamp_instead_of_string_time(self):
        timest = Timest(input_fmt="%Y-%m-%d")
        with self.assertRaises(TimestConversionError):
            timest.utc_time2utc_timetz(time=1531432748, latitude=10, longitude=20)

    def test_raise_timest_conversion_error_when_wrong_format_is_used(self):
        timest = Timest(input_fmt="%Y-%m-%d")
        with self.assertRaises(TimestConversionError):
            timest.utc_time2utc_timetz(time='31-12-2021', latitude=10, longitude=20)

    def test_output_format_string_time(self):
        test_lat = 45.1686197
        test_lng = 9.1561581
        timest = Timest(input_fmt="%Y-%m-%dT%H:%M:%SZ", output_fmt="%d-%m-%Y; %H:%M; %z")
        actual = timest.utc_time2utc_timetz_str(time="2021-10-11T09:44:00Z", latitude=test_lat, longitude=test_lng)
        self.assertEqual(actual, "11-10-2021; 09:44; +0200")

    def test_output_format_timestamp(self):
        test_lat = 40.416774
        test_lng = -3.703790
        timest = Timest(output_fmt="%Y-%m-%d, %z")
        actual = timest.utc_time2utc_timetz_str(time=1551288953, latitude=test_lat, longitude=test_lng)
        self.assertEqual(actual, "2019-02-27, +0100")


if __name__ == '__main__':
    main()
