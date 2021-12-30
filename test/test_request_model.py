######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 15:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.request import AddPurpleairSensorRequest, AddAtmotubeMeasureRequest


class TestRequestModel(TestCase):

    def test_create_request_for_adding_purpleair_sensor(self):
        req = AddPurpleairSensorRequest(
            name="fakename",
            sensor_index=9,
            latitude=1.234,
            longitude=5.666,
            altitude=0,
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

        self.assertEqual(req.name, "fakename")
        self.assertEqual(req.sensor_index, 9)
        self.assertEqual(req.latitude, 1.234)
        self.assertEqual(req.longitude, 5.666)
        self.assertEqual(req.altitude, 0)
        self.assertEqual(req.primary_id_a, 111)
        self.assertEqual(req.primary_key_a, "key1a")
        self.assertEqual(req.primary_id_b, 222)
        self.assertEqual(req.primary_key_b, "key1b")
        self.assertEqual(req.secondary_id_a, 333)
        self.assertEqual(req.secondary_key_a, "key2a")
        self.assertEqual(req.secondary_id_b, 444)
        self.assertEqual(req.secondary_key_b, "key2b")

    def test_create_request_for_adding_atmotube_measure(self):
        req = AddAtmotubeMeasureRequest(
            time="2021-08-10T23:59:00.000Z",
            voc=0.17,
            pm1=8,
            pm25=10,
            pm10=11,
            t=29,
            h=42,
            p=1004.68,
            coords={'lat': 45.765, 'lon': 9.897}
        )

        self.assertEqual(req.time, "2021-08-10T23:59:00.000Z")
        self.assertEqual(req.voc, 0.17)
        self.assertEqual(req.pm1, 8)
        self.assertEqual(req.pm25, 10)
        self.assertEqual(req.pm10, 11)
        self.assertEqual(req.t, 29)
        self.assertEqual(req.h, 42)
        self.assertEqual(req.p, 1004.68)
        self.assertEqual(req.coords, {'lat': 45.765, 'lon': 9.897})


if __name__ == '__main__':
    main()
