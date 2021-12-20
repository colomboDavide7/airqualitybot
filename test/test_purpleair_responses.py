######################################################
#
# Author: Davide Colombo
# Date: 20/12/21 14:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.response import PurpleairResponse
from airquality.respitem import ChannelProperties


class TestPurpleairResponse(TestCase):

    @patch('airquality.response.urlopen')
    def test_successfully_fetch_response(self, mocked_urlopen):
        with open('test_resources/purpleair_response.json') as rf:
            api_response = rf.read()

        mocked_resp = MagicMock()
        mocked_resp.getcode.return_value = 200
        mocked_resp.read.side_effect = [api_response]
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        existing_names = ["n1 (1)", "n2 (2)"]
        responses = PurpleairResponse(url="foo", existing_names=existing_names)
        self.assertEqual(len(responses), 1)
        resp = responses[0]
        self.assertEqual(resp.name(), "n3 (3)")
        self.assertEqual(resp.created_at(), "2018-09-29 23:10:23")
        self.assertEqual(resp.located_at(), "ST_GeomFromText('POINT(9.12 45.24)', 26918)")
        expected_channels = {ChannelProperties(key="key1a3", ident="id1a3", name="1A"),
                             ChannelProperties(key="key1b3", ident="id1b3", name="1B"),
                             ChannelProperties(key="key2a3", ident="id2a3", name="2A"),
                             ChannelProperties(key="key2b3", ident="id2b3", name="2B")}
        self.assertEqual(resp.channel_properties(), expected_channels)

        with self.assertRaises(IndexError):
            print("IndexError caught successfully")
            responses[1]


if __name__ == '__main__':
    main()
