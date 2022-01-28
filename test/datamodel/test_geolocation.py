# ======================================
# @author:  Davide Colombo
# @date:    2022-01-28, ven, 12:08
# ======================================
from unittest import TestCase, main
from airquality.datamodel.geolocation import Geolocation


class TestGeolocation(TestCase):

    def test_create_geolocation_from_tuple_of_float(self):
        actual = Geolocation(row=(9.4673268, 45.12489))
        self.assertEqual(actual.longitude, 9.4673268)
        self.assertEqual(actual.latitude, 45.12489)


if __name__ == '__main__':
    main()
