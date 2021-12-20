######################################################
#
# Author: Davide Colombo
# Date: 20/12/21 14:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.response import PurpleairResponses
from airquality.respitem import ChannelProperties

TEST_PURPLEAIR_RESPONSES = """
{"fields": ["sensor_index", "name", "latitude", "longitude", "altitude", "primary_id_a", "primary_key_a", 
            "primary_id_b", "primary_key_b", "secondary_id_a", "secondary_key_a", "secondary_id_b", "secondary_key_b",
            "date_created"],
 "data": [
        [1, "n1", 45.29, 9.13, 274, "id1a1", "key1a1", "id1b1", "key1b1",  "id2a1", "key2a1", "id2b1", "key2b1", 1531432748],
        [2, "n2", 45.23, 9.11, 274, "id1a2", "key1a2", "id1b2", "key1b2",  "id2a2", "key2a2", "id2b2", "key2b2", 1531432758],
        [3, "n3", 45.24, 9.12, 274, "id1a3", "key1a3", "id1b3", "key1b3",  "id2a3", "key2a3", "id2b3", "key2b3", 1538255423]
    ]
}
"""

TEST_EMPTY_PURPLEAIR_RESPONSES = """
{"fields": ["sensor_index", "name", "latitude", "longitude", "altitude", "primary_id_a", "primary_key_a", 
            "primary_id_b", "primary_key_b", "secondary_id_a", "secondary_key_a", "secondary_id_b", "secondary_key_b",
            "date_created"],
 "data": []
}
"""


class TestPurpleairResponse(TestCase):

    @patch('airquality.response.urlopen')
    def test_successfully_fetch_response(self, mocked_urlopen):
        mocked_resp = MagicMock()
        mocked_resp.getcode.return_value = 200
        mocked_resp.read.side_effect = [TEST_PURPLEAIR_RESPONSES]
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        existing_names = ["n1 (1)", "n2 (2)"]
        responses = PurpleairResponses(url="foo", existing_names=existing_names)
        self.assertEqual(len(responses), 1)
        resp = responses[0]
        self.assertEqual(resp.name, "n3 (3)")
        self.assertEqual(resp.created_at, "2018-09-29 23:10:23")
        self.assertEqual(resp.located_at, "ST_GeomFromText('POINT(9.12 45.24)', 26918)")
        expected_channels = {ChannelProperties(key="key1a3", ident="id1a3", name="1A"),
                             ChannelProperties(key="key1b3", ident="id1b3", name="1B"),
                             ChannelProperties(key="key2a3", ident="id2a3", name="2A"),
                             ChannelProperties(key="key2b3", ident="id2b3", name="2B")}
        self.assertEqual(resp.channel_properties, expected_channels)

        with self.assertRaises(IndexError):
            print("IndexError caught successfully")
            responses[1]

    @patch('airquality.response.urlopen')
    def test_successfully_fetch_empty_response(self, mocked_urlopen):
        mocked_resp = MagicMock()
        mocked_resp.getcode.return_value = 200
        mocked_resp.read.side_effect = [TEST_EMPTY_PURPLEAIR_RESPONSES]
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        existing_names = ["n1 (1)", "n2 (2)"]
        responses = PurpleairResponses(url="foo", existing_names=existing_names)
        self.assertEqual(len(responses), 0)

        with self.assertRaises(IndexError):
            print("IndexError caught successfully")
            responses[0]


if __name__ == '__main__':
    main()
