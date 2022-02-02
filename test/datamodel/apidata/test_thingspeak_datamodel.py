# ======================================
# @author:  Davide Colombo
# @date:    2022-01-20, gio, 19:58
# ======================================
from unittest import TestCase, main
from airquality.datamodel.fromapi import ThingspeakDM


class TestThingspeakDatamodel(TestCase):

    def test_thingspeak_datamodel_channel_1A(self):
        data = ThingspeakDM(
            created_at="2021-12-20T11:18:40Z",
            field1="20.50",
            field2="35.53",
            field3="37.43",
            field6="55",
            field7="60"
        )

        self.assertEqual(data.created_at, "2021-12-20T11:18:40Z")
        self.assertEqual(data.field1, 20.50)
        self.assertEqual(data.field2, 35.53)
        self.assertEqual(data.field3, 37.43)
        self.assertEqual(data.field6, 55)
        self.assertEqual(data.field7, 60)
        self.assertIsNone(data.field4)
        self.assertIsNone(data.field5)

    def test_thingspeak_datamodel_channel_1B(self):
        data = ThingspeakDM(
            created_at="2021-12-19T11:06:25Z",
            field1="126.65",
            field2="222.24",
            field3="283.44",
            field6="1016.49",
        )
        self.assertEqual(data.created_at, "2021-12-19T11:06:25Z")
        self.assertEqual(data.field1, 126.65)
        self.assertEqual(data.field2, 222.24)
        self.assertEqual(data.field3, 283.44)
        self.assertEqual(data.field6, 1016.49)
        self.assertIsNone(data.field7)
        self.assertIsNone(data.field4)
        self.assertIsNone(data.field5)

    def test_thingspeak_datamodel_channel_2A(self):
        data = ThingspeakDM(
            created_at="2021-12-19T11:06:23Z",
            field1="10544.95",
            field2="2980.84",
            field3="724.11",
            field4="127.53",
            field5="28.51",
            field6="2.25",
        )
        self.assertEqual(data.created_at, "2021-12-19T11:06:23Z")
        self.assertEqual(data.field1, 10544.95)
        self.assertEqual(data.field2, 2980.84)
        self.assertEqual(data.field3, 724.11)
        self.assertEqual(data.field4, 127.53)
        self.assertEqual(data.field5, 28.51)
        self.assertEqual(data.field6, 2.25)
        self.assertIsNone(data.field7)

    def test_thingspeak_datamodel_channel_2B(self):
        data = ThingspeakDM(
            created_at="2021-12-09T15:54:34Z",
            field1="10544.95",
            field2="2980.84",
            field3="724.11",
            field4="127.53",
            field5="28.51",
            field6="2.25",
        )
        self.assertEqual(data.created_at, "2021-12-09T15:54:34Z")
        self.assertEqual(data.field1, 10544.95)
        self.assertEqual(data.field2, 2980.84)
        self.assertEqual(data.field3, 724.11)
        self.assertEqual(data.field4, 127.53)
        self.assertEqual(data.field5, 28.51)
        self.assertEqual(data.field6, 2.25)
        self.assertIsNone(data.field7)


if __name__ == '__main__':
    main()
