######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 11:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.api.resp.info as resp


class TestInfoResponse(unittest.TestCase):

    def setUp(self) -> None:
        self.purpleair_info_resp_builder = resp.PurpleairSensorInfoBuilder()

    def test_successfully_build_purpleair_api_response(self):
        test_response = {
            'fields': ["sensor_index", "name", "latitude", "longitude", "primary_id_a", "primary_key_a", "primary_id_b",
                       "primary_key_b", "secondary_id_a", "secondary_key_a", "secondary_id_b", "secondary_key_b",
                       "date_created"],
            'data': [
                ["idx1", "n1", "lat", "lon", "id_1a", "key_1a", "id_1b", "key_1b", "id_2a", "key_2a", "id_2b", "key_2b", 1531432748]
            ]
        }
        # Build the response
        actual = self.purpleair_info_resp_builder.build(test_response)
        first_response = actual[0]
        self.assertEqual(first_response.sensor_name, "n1 (idx1)")
        self.assertEqual(first_response.sensor_type, resp.PurpleairSensorInfoBuilder.TYPE)
        self.assertEqual(first_response.geolocation.geometry.as_text(), "POINT(lon lat)")

        # Test channel values
        self.assertEqual(len(first_response.channels), 4)

        # *********************************************
        #
        # THE FACT THAT THE FIRST CHANNEL CORRESPOND TO 'id_1a' AND SECOND CHANNEL TO 'id_1b' AND SO ON...
        # AND THE SUCCESS OF THIS TEST DEPENDS ON THE ORDER OF THE CHANNELS WITHIN THE 'CHANNEL_PARAM' CLASS VARIABLE
        # WITHIN 'PurpleairSensorInfoBuilder' class
        #
        # *********************************************

        # First channel item
        first_channel = first_response.channels[0]
        self.assertEqual(first_channel.ch_id, "id_1a")
        self.assertEqual(first_channel.ch_key, "key_1a")

        # Second channel item
        second_channel = first_response.channels[1]
        self.assertEqual(second_channel.ch_id, "id_1b")
        self.assertEqual(second_channel.ch_key, "key_1b")

        # Third channel item
        third_channel = first_response.channels[2]
        self.assertEqual(third_channel.ch_id, "id_2a")
        self.assertEqual(third_channel.ch_key, "key_2a")

        # Third channel item
        fourth_channel = first_response.channels[3]
        self.assertEqual(fourth_channel.ch_id, "id_2b")
        self.assertEqual(fourth_channel.ch_key, "key_2b")

    def test_system_exit_on_missing_date_created(self):
        test_response = {
            'fields': ["sensor_index", "name", "latitude", "longitude", "primary_id_a", "primary_key_a", "primary_id_b",
                       "primary_key_b", "secondary_id_a", "secondary_key_a", "secondary_id_b", "secondary_key_b"],
            'data': [
                ["idx1", "n1", "lat", "lon", "id_1a", "key_1a", "id_1b", "key_1b", "id_2a", "key_2a", "id_2b", "key_2b"]
            ]
        }

        with self.assertRaises(SystemExit):
            self.purpleair_info_resp_builder.build(test_response)

    def test_system_exit_on_missing_sensor_name_or_index(self):
        test_missing_sensor_index = {
            'fields': ["name", "latitude", "longitude", "primary_id_a", "primary_key_a", "primary_id_b",
                       "primary_key_b", "secondary_id_a", "secondary_key_a", "secondary_id_b", "secondary_key_b",
                       "date_created"],
            'data': [
                ["n1", "lat", "lon", "id_1a", "key_1a", "id_1b", "key_1b", "id_2a", "key_2a", "id_2b", "key_2b", 1531432748]
            ]
        }
        with self.assertRaises(SystemExit):
            self.purpleair_info_resp_builder.build(test_missing_sensor_index)

        test_missing_name_field = {
            'fields': ["sensor_index", "latitude", "longitude", "primary_id_a", "primary_key_a", "primary_id_b",
                       "primary_key_b", "secondary_id_a", "secondary_key_a", "secondary_id_b", "secondary_key_b",
                       "date_created"],
            'data': [
                ["idx1", "lat", "lon", "id_1a", "key_1a", "id_1b", "key_1b", "id_2a", "key_2a", "id_2b", "key_2b", 1531432748]
            ]
        }

        with self.assertRaises(SystemExit):
            self.purpleair_info_resp_builder.build(test_missing_name_field)

    def test_system_exit_on_missing_primary_channel_a_fields(self):
        test_missing_id_1a_field = {
            'fields': ["sensor_index", "name", "latitude", "longitude", "primary_key_a", "primary_id_b",
                       "primary_key_b", "secondary_id_a", "secondary_key_a", "secondary_id_b", "secondary_key_b",
                       "date_created"],
            'data': [
                ["idx1", "n1", "lat", "lon", "key_1a", "id_1b", "key_1b", "id_2a", "key_2a", "id_2b", "key_2b", 1531432748]
            ]
        }
        with self.assertRaises(SystemExit):
            self.purpleair_info_resp_builder.build(test_missing_id_1a_field)

        test_missing_key_1a_field = {
            'fields': ["sensor_index", "name", "latitude", "longitude", "primary_id_a", "primary_id_b",
                       "primary_key_b", "secondary_id_a", "secondary_key_a", "secondary_id_b", "secondary_key_b",
                       "date_created"],
            'data': [
                ["idx1", "n1", "lat", "lon", "id_1a", "id_1b", "key_1b", "id_2a", "key_2a", "id_2b", "key_2b", 1531432748]
            ]
        }
        with self.assertRaises(SystemExit):
            self.purpleair_info_resp_builder.build(test_missing_key_1a_field)


if __name__ == '__main__':
    unittest.main()
