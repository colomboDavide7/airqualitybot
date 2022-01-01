######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 15:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.datamodel.apidata import PurpleairAPIData, AtmotubeAPIData, ThingspeakPrimaryChannelAData


class TestDatamodel(TestCase):

    def test_purpleair_apidata_model(self):
        data = PurpleairAPIData(
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

        self.assertEqual(data.name, "fakename")
        self.assertEqual(data.sensor_index, 9)
        self.assertEqual(data.latitude, 1.234)
        self.assertEqual(data.longitude, 5.666)
        self.assertEqual(data.altitude, 0)
        self.assertEqual(data.primary_id_a, 111)
        self.assertEqual(data.primary_key_a, "key1a")
        self.assertEqual(data.primary_id_b, 222)
        self.assertEqual(data.primary_key_b, "key1b")
        self.assertEqual(data.secondary_id_a, 333)
        self.assertEqual(data.secondary_key_a, "key2a")
        self.assertEqual(data.secondary_id_b, 444)
        self.assertEqual(data.secondary_key_b, "key2b")

    def test_atmotube_apidata_model(self):
        data = AtmotubeAPIData(
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

        self.assertEqual(data.time, "2021-08-10T23:59:00.000Z")
        self.assertEqual(data.voc, 0.17)
        self.assertEqual(data.pm1, 8)
        self.assertEqual(data.pm25, 10)
        self.assertEqual(data.pm10, 11)
        self.assertEqual(data.t, 29)
        self.assertEqual(data.h, 42)
        self.assertEqual(data.p, 1004.68)
        self.assertEqual(data.coords, {'lat': 45.765, 'lon': 9.897})

    def test_thingspeak_primary_channel_a_apidata_model(self):
        data = ThingspeakPrimaryChannelAData(
            created_at="2021-12-20T11:18:40Z",
            field1="20.50",
            field2="35.53",
            field3="37.43",
            field6="55",
            field7="60"
        )

        self.assertEqual(data.field1, 20.50)
        self.assertEqual(data.field2, 35.53)
        self.assertEqual(data.field3, 37.43)
        self.assertEqual(data.field6, 55)
        self.assertEqual(data.field7, 60)


if __name__ == '__main__':
    main()
