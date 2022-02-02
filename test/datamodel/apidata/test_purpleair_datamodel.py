# ======================================
# @author:  Davide Colombo
# @date:    2022-01-20, gio, 19:55
# ======================================
from unittest import TestCase, main
from airquality.datamodel.fromapi import PurpleairDM


class TestPurpleairDatamodel(TestCase):

    def test_purpleair_apidata_model(self):
        data = PurpleairDM(
            name="fakename",
            sensor_index=9,
            latitude=40,
            longitude=18,
            primary_id_a=111,
            primary_key_a="key1a",
            primary_id_b=222,
            primary_key_b="key1b",
            secondary_id_a=333,
            secondary_key_a="key2a",
            secondary_id_b=444,
            secondary_key_b="key2b",
            date_created=1234567890
        )

        self.assertEqual(data.name, "fakename")
        self.assertEqual(data.sensor_index, 9)
        self.assertEqual(data.primary_id_a, 111)
        self.assertEqual(data.latitude, 40.0)
        self.assertEqual(data.longitude, 18.0)
        self.assertEqual(data.primary_key_a, "key1a")
        self.assertEqual(data.primary_id_b, 222)
        self.assertEqual(data.primary_key_b, "key1b")
        self.assertEqual(data.secondary_id_a, 333)
        self.assertEqual(data.secondary_key_a, "key2a")
        self.assertEqual(data.secondary_id_b, 444)
        self.assertEqual(data.secondary_key_b, "key2b")


if __name__ == '__main__':
    main()
