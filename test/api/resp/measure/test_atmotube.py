######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 15:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import source.api.resp.measure.atmotube as resp


class TestMeasureResponse(unittest.TestCase):

    def setUp(self) -> None:
        self.response_builder = resp.AtmotubeAPIRespBuilder()

    def test_successfully_get_measures(self):
        self.response_builder.with_channel_name("main")
        test_item = {"voc": 0.88, "t": 22}

        actual = self.response_builder.get_measures(test_item)
        self.assertEqual(actual[0].name, "voc")
        self.assertEqual(actual[0].value, 0.88)
        self.assertEqual(actual[1].name, "pm1")
        self.assertEqual(actual[1].value, None)
        self.assertEqual(actual[2].name, "pm25")
        self.assertEqual(actual[2].value, None)
        self.assertEqual(actual[3].name, "pm10")
        self.assertEqual(actual[3].value, None)
        self.assertEqual(actual[4].name, "t")
        self.assertEqual(actual[4].value, 22)
        self.assertEqual(actual[5].name, "h")
        self.assertEqual(actual[5].value, None)
        self.assertEqual(actual[6].name, "p")
        self.assertEqual(actual[6].value, None)

    def test_successfully_get_geometry(self):
        test_item = {"coords": {"lat": "l1", "lon": "l2"}}
        actual = self.response_builder.get_geometry(test_item)
        self.assertEqual(actual.as_text(), "POINT(l2 l1)")

    def test_null_geometry_when_coords_are_missing(self):
        test_item = {"some_arg": 2}
        actual = self.response_builder.get_geometry(test_item)
        self.assertEqual(actual.as_text(), "NULL")

    ################################ TEST EXIT ON BAD ITEM ################################
    def test_successfully_check_item(self):
        test_item = {"time": "some_timestamp"}
        self.response_builder.exit_on_bad_item(test_item)
        self.assertTrue(True)

    def test_exit_on_missing_item_timestamp(self):
        with self.assertRaises(SystemExit):
            self.response_builder.build({"some_key": "some_value"})

    ################################ TEST EXIT ON BAD PARSED RESPONSE ################################
    def test_successfully_check_parsed_response(self):
        test_parsed_resp = {"data": {"items": []}}
        self.response_builder.exit_on_bad_parsed_response(test_parsed_resp)
        self.assertTrue(True)

    def test_exit_on_missing_response_data_section(self):
        test_parsed_resp = {"some_section": ""}
        with self.assertRaises(SystemExit):
            self.response_builder.exit_on_bad_parsed_response(test_parsed_resp)

    def test_exit_on_missing_response_items(self):
        test_parsed_resp = {"data": {"some_section": ""}}
        with self.assertRaises(SystemExit):
            self.response_builder.exit_on_bad_parsed_response(test_parsed_resp)


if __name__ == '__main__':
    unittest.main()
