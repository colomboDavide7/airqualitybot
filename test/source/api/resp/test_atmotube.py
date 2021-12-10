######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 15:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import api.resp.atmotube as resptype


class TestMeasureResponse(unittest.TestCase):

    def setUp(self) -> None:
        self.response_builder = resptype.AtmotubeAPIRespBuilder(channel_name="main")

    def test_successfully_get_measures(self):
        test_item = {"data": {"items": [{"voc": 0.88, "t": 22}]}}

        actual = self.response_builder.build(test_item)
        measures = actual[0].measures
        self.assertEqual(measures[0].name, "voc")
        self.assertEqual(measures[0].value, 0.88)
        self.assertEqual(measures[1].name, "pm1")
        self.assertEqual(measures[1].value, None)
        self.assertEqual(measures[2].name, "pm25")
        self.assertEqual(measures[2].value, None)
        self.assertEqual(measures[3].name, "pm10")
        self.assertEqual(measures[3].value, None)
        self.assertEqual(measures[4].name, "t")
        self.assertEqual(measures[4].value, 22)
        self.assertEqual(measures[5].name, "h")
        self.assertEqual(measures[5].value, None)
        self.assertEqual(measures[6].name, "p")
        self.assertEqual(measures[6].value, None)

    def test_successfully_get_geometry(self):
        test_item = {"data": {"items": [{"coords": {"lat": "l1", "lon": "l2"}}]}}
        actual = self.response_builder.build(test_item)
        geolocation = actual[0].geolocation
        self.assertEqual(geolocation.latitude, "l1")
        self.assertEqual(geolocation.longitude, "l2")

    def test_null_geometry_when_coords_are_missing(self):
        test_item = {"data": {"items": [{"some_arg": 2}]}}
        actual = self.response_builder.build(test_item)
        geolocation = actual[0].geolocation
        self.assertIsNone(geolocation)

    ################################ TEST EXIT ON BAD ITEM ################################
    def test_exit_on_missing_item_timestamp(self):
        with self.assertRaises(SystemExit):
            self.response_builder.build({"some_key": "some_value"})

    ################################ TEST EXIT ON BAD PARSED RESPONSE ################################
    def test_empty_list_when_response_is_empty(self):
        test_parsed_resp = {"data": {"items": []}}
        actual = self.response_builder.build(test_parsed_resp)
        self.assertEqual(len(actual), 0)

    def test_exit_on_missing_response_data_section(self):
        test_parsed_resp = {"some_section": ""}
        with self.assertRaises(SystemExit):
            self.response_builder.build(test_parsed_resp)

    def test_exit_on_missing_response_items(self):
        test_parsed_resp = {"data": {"some_section": ""}}
        with self.assertRaises(SystemExit):
            self.response_builder.build(test_parsed_resp)


if __name__ == '__main__':
    unittest.main()
