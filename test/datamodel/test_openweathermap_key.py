######################################################
#
# Author: Davide Colombo
# Date: 03/01/22 20:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.datamodel.openweathermap_key import OpenweathermapKey


def _expected_repr():
    return "OpenweathermapKey(key_value=XXX, done_requests_per_minute=0, max_requests_per_minute=60)"


class TestServiceParam(TestCase):

    def test_service_param(self):
        key = OpenweathermapKey(
            key_value="some_key",
            done_requests_per_minute=0,
            max_requests_per_minute=60
        )
        self.assertEqual(key.key_value, "some_key")
        self.assertEqual(key.done_requests_per_minute, 0)
        self.assertEqual(key.max_requests_per_minute, 60)
        self.assertEqual(repr(key), _expected_repr())


if __name__ == '__main__':
    main()
