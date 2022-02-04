######################################################
#
# Author: Davide Colombo
# Date: 03/01/22 20:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.datamodel.fromdb import OpenweathermapKeyDM


class TestServiceParam(TestCase):

    def test_openweathermap_key_datamodel(self):
        key = OpenweathermapKeyDM(
            key="some_key",
            n_done=0,
            n_max=60
        )
        self.assertEqual(key.key, "some_key")
        self.assertEqual(key.n_done, 0)
        self.assertEqual(key.n_max, 60)


if __name__ == '__main__':
    main()
