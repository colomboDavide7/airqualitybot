######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 11:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.api.resp.info.purpleair as resp


class TestInfoResponse(unittest.TestCase):

    def setUp(self) -> None:
        self.resp_builder = resp.PurpleairAPIRespBuilder()

    def test_get_geolocation(self):
        test_item = {"longitude": "l1", "latitude": "l2"}
        actual = self.resp_builder.get_geolocation(test_item)
        self.assertEqual(actual.geometry.as_text(), "POINT(l1 l2)")

    def test_get_sensor_name(self):
        test_item = {"sensor_index": "idx1", "name": "n1"}
        actual = self.resp_builder.get_sensor_name(test_item)
        expected = "n1 (idx1)"
        self.assertEqual(actual, expected)

    def test_get_channels(self):
        test_item = {"primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
                     "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b", "secondary_key_b": "key2b",
                     "date_created": 1531432748}
        actual = self.resp_builder.get_channels(test_item)

        first_channel = actual[0]
        self.assertEqual(first_channel.ch_id, "id1a")
        self.assertEqual(first_channel.ch_key, "key1a")

        second_channel = actual[1]
        self.assertEqual(second_channel.ch_id, "id1b")
        self.assertEqual(second_channel.ch_key, "key1b")

        third_channel = actual[2]
        self.assertEqual(third_channel.ch_id, "id2a")
        self.assertEqual(third_channel.ch_key, "key2a")

        fourth_channel = actual[3]
        self.assertEqual(fourth_channel.ch_id, "id2b")
        self.assertEqual(fourth_channel.ch_key, "key2b")

    ################################ TEST EXIT ON BAD ITEM ################################
    def test_successfully_check_item(self):
        test_item = {"sensor_index": "idx1", "name": "n1", "date_created": "some_date", "latitude": "l1", "longitude": "l2",
                     "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
                     "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b", "secondary_key_b": "key2b"}
        self.resp_builder.exit_on_bad_item(test_item)
        self.assertTrue(True)

    def test_exit_on_missing_item_name(self):
        test_item = {"sensor_index": "idx1", "date_created": "some_date", "latitude": "l1",
                     "longitude": "l2",
                     "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
                     "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b",
                     "secondary_key_b": "key2b"}

        with self.assertRaises(SystemExit):
            self.resp_builder.exit_on_bad_item(test_item)

    def test_exit_on_missing_sensor_index_item(self):
        test_item = {"name": "n1", "date_created": "some_date", "latitude": "l1",
                     "longitude": "l2",
                     "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
                     "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b",
                     "secondary_key_b": "key2b"}

        with self.assertRaises(SystemExit):
            self.resp_builder.exit_on_bad_item(test_item)

    def test_exit_on_missing_latitude_item(self):
        test_item = {"sensor_index": "idx1", "name": "n1", "date_created": "some_date", "longitude": "l2",
                     "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
                     "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b",
                     "secondary_key_b": "key2b"}

        with self.assertRaises(SystemExit):
            self.resp_builder.exit_on_bad_item(test_item)

    def test_exit_on_missing_longitude_item(self):
        test_item = {"sensor_index": "idx1", "name": "n1", "date_created": "some_date", "latitude": "l2",
                     "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
                     "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b",
                     "secondary_key_b": "key2b"}

        with self.assertRaises(SystemExit):
            self.resp_builder.exit_on_bad_item(test_item)

    def test_exit_on_missing_date_created_item(self):
        test_item = {"sensor_index": "idx1", "name": "n1", "latitude": "l1", "longitude": "l2",
                     "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
                     "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b",
                     "secondary_key_b": "key2b"}

        with self.assertRaises(SystemExit):
            self.resp_builder.exit_on_bad_item(test_item)

    ################################ TEST EXIT ON BAD PARSED RESPONSE ################################
    def test_successfully_check_parsed_response(self):
        test_response = {"fields": [], "data": []}
        self.resp_builder.exit_on_bad_parsed_response(test_response)
        self.assertTrue(True)

    def test_exit_on_missing_response_fields_section(self):
        test_response = {"data": []}
        with self.assertRaises(SystemExit):
            self.resp_builder.exit_on_bad_parsed_response(test_response)

    def test_exit_on_missing_response_data_section(self):
        test_response = {"fields": []}
        with self.assertRaises(SystemExit):
            self.resp_builder.exit_on_bad_parsed_response(test_response)


if __name__ == '__main__':
    unittest.main()
