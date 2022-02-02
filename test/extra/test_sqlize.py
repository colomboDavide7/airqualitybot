# ======================================
# @author:  Davide Colombo
# @date:    2022-02-2, mer, 08:03
# ======================================
from datetime import datetime
import test._test_utils as tutils
from unittest import TestCase, main
from airquality.extra.sqlize import sqlize


def _timezone_info():
    return tutils.get_tzinfo_from_timezone_name(tzname="America/New York")


def _iterable():
    return 1, None, datetime(2022, 1, 24, 10, 37, tzinfo=_timezone_info()), 'Hello'


class TestSQLizeIterable(TestCase):

    def test_sqlize_tuple(self):
        self.assertEqual(
            sqlize(iterable=_iterable()),
            "(1,NULL,'2022-01-24 10:37:00-05:00','Hello')"
        )


if __name__ == '__main__':
    main()
