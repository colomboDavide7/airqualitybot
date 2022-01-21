######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 14:26
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.url.timeiter_url import AtmotubeTimeIterableURL, ThingspeakTimeIterableURL
from unittest import TestCase, main
from datetime import datetime


# ======================================== THINGSPEAK TESTS ========================================
def _expected_thingspeak_repr():
    return "ThingspeakTimeIterableURL(" \
           "url='some_url', " \
           "begin='2021-12-01 00:00:00', " \
           "until='2021-12-29 17:44:35', " \
           "step_size_in_days='7')"


class TestThingspeakTimeIterableURL(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._begin = datetime.strptime('2021-12-01 00:00:00', "%Y-%m-%d %H:%M:%S")
        self._until = datetime.strptime('2021-12-29 17:44:35', "%Y-%m-%d %H:%M:%S")
        self._urls = ThingspeakTimeIterableURL(url="some_url",
                                               begin=self._begin,
                                               until=self._until,
                                               step_size_in_days=7)

# =========== TEST METHODS
    def test_thingspeak_url_formatter(self):
        self.assertEqual(len(self._urls), 5)
        self.assertEqual(self._urls[0], "some_url&start=2021-12-01%2000:00:00&end=2021-12-08%2000:00:00")
        self.assertEqual(self._urls[1], "some_url&start=2021-12-08%2000:00:00&end=2021-12-15%2000:00:00")
        self.assertEqual(self._urls[2], "some_url&start=2021-12-15%2000:00:00&end=2021-12-22%2000:00:00")
        self.assertEqual(self._urls[3], "some_url&start=2021-12-22%2000:00:00&end=2021-12-29%2000:00:00")
        self.assertEqual(self._urls[4], "some_url&start=2021-12-29%2000:00:00&end=2021-12-29%2017:44:35")
        self.assertEqual(repr(self._urls), _expected_thingspeak_repr())
        with self.assertRaises(IndexError):
            print(self._urls[5])


# ======================================== ATMOTUBE TESTS ========================================
def _expected_atmotube_repr():
    return "AtmotubeTimeIterableURL(" \
           "url='some_url', " \
           "begin='2021-12-01 00:00:00', " \
           "until='2021-12-03 17:44:35', " \
           "step_size_in_days='1')"


class TestAtmotubeTimeIterableURL(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._begin = datetime.strptime('2021-12-01 00:00:00', "%Y-%m-%d %H:%M:%S")
        self._until = datetime.strptime('2021-12-03 17:44:35', "%Y-%m-%d %H:%M:%S")
        self._urls = AtmotubeTimeIterableURL(url="some_url",
                                             begin=self._begin,
                                             until=self._until,
                                             step_size_in_days=1)

# =========== TEST METHODS
    def test_urls(self):
        self.assertEqual(len(self._urls), 3)
        self.assertEqual(self._urls[0], "some_url&date=2021-12-01")
        self.assertEqual(self._urls[1], "some_url&date=2021-12-02")
        self.assertEqual(self._urls[2], "some_url&date=2021-12-03")
        self.assertEqual(repr(self._urls), _expected_atmotube_repr())
        with self.assertRaises(IndexError):
            print(self._urls[3])


if __name__ == '__main__':
    main()
