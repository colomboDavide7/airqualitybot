# ======================================
# @author:  Davide Colombo
# @date:    2022-02-2, mer, 08:03
# ======================================
from datetime import datetime
import test._test_utils as tutils
from unittest import TestCase, main
from airquality.extra.sqlize import sqlize_iterable, sqlize_obj


def _timezone_info():
    return tutils.get_tzinfo_from_timezone_name(tzname="America/New York")


def _iterable():
    return 1, None, datetime(2022, 1, 24, 10, 37, tzinfo=_timezone_info()), 'Hello'


def _attributes():
    return [
        'name',
        'type'
    ]


def _reversed_attributes():
    return [
        'type',
        'name',
    ]


def _bad_attributes():
    return [
        'name',
        'type',
        'badattr'
    ]


def _obj():
    class TestObj(object):
        def __init__(self, name, type_):
            self.name = name
            self.type = type_
    return TestObj(name='n1', type_='t1')


class TestSqlizeIterable(TestCase):

    def test_sqlize_tuple(self):
        self.assertEqual(
            sqlize_iterable(_iterable()),
            "(1,NULL,'2022-01-24 10:37:00-05:00','Hello')"
        )

    def test_sqlize_object(self):
        test_obj = _obj()
        actual = sqlize_obj(
            self=test_obj,
            attributes=_attributes(),
            header='('
        )
        self.assertEqual(actual, "('n1','t1')")

    def test_sqlize_object_with_attributes_in_different_order(self):
        test_obj = _obj()
        actual = sqlize_obj(
            self=test_obj,
            attributes=_reversed_attributes()
        )
        self.assertEqual(actual, "('t1','n1')")

    def test_raise_attribute_error_if_try_to_sqlize_object_with_wrong_attribute_list(self):
        test_obj = _obj()
        with self.assertRaises(AttributeError):
            sqlize_obj(self=test_obj, attributes=_bad_attributes(), header='(')

    def test_sqlize_object_with_header_and_teardown(self):
        test_obj = _obj()
        actual = sqlize_obj(
            self=test_obj,
            attributes=_reversed_attributes(),
            header='(12, 33, ',
            teardown=', hi)'
        )
        self.assertEqual(actual, "(12, 33,'t1','n1',hi)")

    def test_sqlize_object_with_bad_header_and_teardown(self):
        test_obj = _obj()
        actual = sqlize_obj(
            self=test_obj,
            attributes=_attributes(),
            header='  ,,, 12, 33,  ',
            teardown='  ,,, hi,  '
        )
        self.assertEqual(actual, "(12, 33,'n1','t1',hi)")


if __name__ == '__main__':
    main()
