######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 11:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import api.resp.purpleair as resptype


class TestInfoResponse(unittest.TestCase):

    def setUp(self) -> None:
        self.resp_builder = resptype.PurpleairAPIRespBuilder()

    def test_date_created(self):
        test_response = {"fields": ["date_created"], "data": [[1531432748]]}
        actual = self.resp_builder.build(test_response)
        date_created = actual[0].date_created
        self.assertEqual(date_created, 1531432748)

    def test_get_geolocation(self):
        test_item = {"fields": ["latitude", "longitude"], "data": [["l1", "l2"]]}
        actual = self.resp_builder.build(test_item)
        geolocation = actual[0].geolocation
        self.assertEqual(geolocation.longitude, "l2")
        self.assertEqual(geolocation.latitude, "l1")

    def test_get_sensor_name(self):
        test_item = {"fields": ["sensor_index", "name"], "data": [["idx1", "n1"]]}
        actual = self.resp_builder.build(test_item)
        self.assertEqual(actual[0].name, "n1")
        self.assertEqual(actual[0].sensor_index, "idx1")

    def test_get_channels(self):
        test_item = {"fields": ["primary_id_a", "primary_key_a", "primary_id_b", "primary_key_b",
                                "secondary_id_a", "secondary_key_a", "secondary_id_b", "secondary_key_b"],
                     "data": [["id1a", "key1a", "id1b", "key1b", "id2a", "key2a", "id2b", "key2b"]]}

        actual = self.resp_builder.build(test_item)
        channels = actual[0].channels

        first_channel = channels[0]
        self.assertEqual(first_channel.ident, "id1a")
        self.assertEqual(first_channel.key, "key1a")

        second_channel = channels[1]
        self.assertEqual(second_channel.ident, "id1b")
        self.assertEqual(second_channel.key, "key1b")

        third_channel = channels[2]
        self.assertEqual(third_channel.ident, "id2a")
        self.assertEqual(third_channel.key, "key2a")

        fourth_channel = channels[3]
        self.assertEqual(fourth_channel.ident, "id2b")
        self.assertEqual(fourth_channel.key, "key2b")

    # ################################ TEST EXIT ON BAD ITEM ################################
    # def test_successfully_check_item(self):
    #     test_item = {"sensor_index": "idx1", "name": "n1", "date_created": "some_date", "latitude": "l1", "longitude": "l2",
    #                  "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
    #                  "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b", "secondary_key_b": "key2b"}
    #     self.resp_builder.exit_on_bad_item(test_item)
    #     self.assertTrue(True)
    #
    # def test_exit_on_missing_item_name(self):
    #     test_item = {"sensor_index": "idx1", "date_created": "some_date", "latitude": "l1",
    #                  "longitude": "l2",
    #                  "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
    #                  "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b",
    #                  "secondary_key_b": "key2b"}
    #
    #     with self.assertRaises(SystemExit):
    #         self.resp_builder.exit_on_bad_item(test_item)
    #
    # def test_exit_on_missing_sensor_index_item(self):
    #     test_item = {"name": "n1", "date_created": "some_date", "latitude": "l1",
    #                  "longitude": "l2",
    #                  "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
    #                  "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b",
    #                  "secondary_key_b": "key2b"}
    #
    #     with self.assertRaises(SystemExit):
    #         self.resp_builder.exit_on_bad_item(test_item)
    #
    # def test_exit_on_missing_latitude_item(self):
    #     test_item = {"sensor_index": "idx1", "name": "n1", "date_created": "some_date", "longitude": "l2",
    #                  "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
    #                  "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b",
    #                  "secondary_key_b": "key2b"}
    #
    #     with self.assertRaises(SystemExit):
    #         self.resp_builder.exit_on_bad_item(test_item)
    #
    # def test_exit_on_missing_longitude_item(self):
    #     test_item = {"sensor_index": "idx1", "name": "n1", "date_created": "some_date", "latitude": "l2",
    #                  "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
    #                  "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b",
    #                  "secondary_key_b": "key2b"}
    #
    #     with self.assertRaises(SystemExit):
    #         self.resp_builder.exit_on_bad_item(test_item)
    #
    # def test_exit_on_missing_date_created_item(self):
    #     test_item = {"sensor_index": "idx1", "name": "n1", "latitude": "l1", "longitude": "l2",
    #                  "primary_id_a": "id1a", "primary_key_a": "key1a", "primary_id_b": "id1b", "primary_key_b": "key1b",
    #                  "secondary_id_a": "id2a", "secondary_key_a": "key2a", "secondary_id_b": "id2b",
    #                  "secondary_key_b": "key2b"}
    #
    #     with self.assertRaises(SystemExit):
    #         self.resp_builder.exit_on_bad_item(test_item)

    ################################ TEST EXIT ON BAD PARSED RESPONSE ################################
    def test_empty_list_when_response_is_empty(self):
        test_response = {"fields": [], "data": []}
        actual = self.resp_builder.build(test_response)
        self.assertEqual(len(actual), 0)

    def test_exit_on_missing_response_fields_section(self):
        test_response = {"data": []}
        with self.assertRaises(SystemExit):
            self.resp_builder.build(test_response)

    def test_exit_on_missing_response_data_section(self):
        test_response = {"fields": []}
        with self.assertRaises(SystemExit):
            self.resp_builder.build(test_response)


if __name__ == '__main__':
    unittest.main()
