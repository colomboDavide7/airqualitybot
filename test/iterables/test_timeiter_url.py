######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 14:26
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.iterables.urls import AtmotubeIterableUrls, ThingspeakIterableUrls
from unittest import TestCase, main
import test._test_utils as tutils
from datetime import datetime


def _rome_timezone():
    return tutils.get_tzinfo_from_timezone_name(tzname='Europe/Rome')


def _new_york_timezone():
    return tutils.get_tzinfo_from_timezone_name(tzname='America/New_York')


# ======================================== THINGSPEAK TESTS ========================================
def _expected_thingspeak_repr():
    return "ThingspeakIterableUrls(" \
           "url='some_url', " \
           "begin='2021-12-01 07:46:00', " \
           "until='2021-12-29 07:10:00', " \
           "step_size_in_days='7')"


class TestThingspeakTimeIterableURL(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._begin = datetime(2021, 12, 1, 2, 46, tzinfo=_new_york_timezone())
        self._until = datetime(2021, 12, 29, 8, 10, tzinfo=_rome_timezone())
        self._urls = ThingspeakIterableUrls(url="some_url",
                                            begin=self._begin,
                                            until=self._until,
                                            step_size_in_days=7)

# =========== TEST METHODS
    def test_thingspeak_url_formatter(self):
        self.assertEqual(
            len(self._urls),
            4
        )
        self.assertEqual(
            self._urls[0],
            "some_url&start=2021-12-01%2007:46:00&end=2021-12-08%2007:46:00"
        )
        self.assertEqual(
            self._urls[1],
            "some_url&start=2021-12-08%2007:46:00&end=2021-12-15%2007:46:00"
        )
        self.assertEqual(
            self._urls[2],
            "some_url&start=2021-12-15%2007:46:00&end=2021-12-22%2007:46:00"
        )
        self.assertEqual(
            self._urls[3],
            "some_url&start=2021-12-22%2007:46:00&end=2021-12-29%2007:10:00"
        )
        self.assertEqual(
            repr(self._urls),
            _expected_thingspeak_repr()
        )
        with self.assertRaises(IndexError):
            print(self._urls[4])


# ======================================== ATMOTUBE TESTS ========================================
def _expected_atmotube_repr():
    return "AtmotubeIterableUrls(" \
           "url='some_url', " \
           "begin='2021-12-01 07:10:00', " \
           "until='2021-12-03 15:10:00', " \
           "step_size_in_days='1')"


class TestAtmotubeTimeIterableURL(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._begin = datetime(2021, 12, 1, 8, 10, tzinfo=_rome_timezone())
        self._until = datetime(2021, 12, 3, 10, 10, tzinfo=_new_york_timezone())
        self._urls = AtmotubeIterableUrls(url="some_url",
                                          begin=self._begin,
                                          until=self._until,
                                          step_size_in_days=1)

# =========== TEST METHODS
    def test_urls(self):
        self.assertEqual(
            len(self._urls),
            3
        )
        self.assertEqual(
            self._urls[0],
            "some_url&date=2021-12-01"
        )
        self.assertEqual(
            self._urls[1],
            "some_url&date=2021-12-02"
        )
        self.assertEqual(
            self._urls[2],
            "some_url&date=2021-12-03"
        )
        self.assertEqual(
            repr(self._urls),
            _expected_atmotube_repr()
        )
        with self.assertRaises(IndexError):
            print(self._urls[3])


if __name__ == '__main__':
    main()
