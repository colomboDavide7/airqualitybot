# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 20:09
# ======================================
from requests.exceptions import HTTPError
from unittest import TestCase, main
from unittest.mock import patch, MagicMock
from airquality.url.api_server_wrap import APIServerWrapper, BadAPIServerResponseError


class TestAPIServerWrapper(TestCase):

    @property
    def get_test_json_response(self):
        return {'p1': 'a1', 'p2': 'a2'}

    @patch('airquality.url.api_server_wrap.requests.get')
    def test_successfully_get_response_from_server(self, mocked_get):

        mocked_response = MagicMock()
        mocked_response.json.return_value = self.get_test_json_response
        mocked_response.status_code = 200
        mocked_get.return_value = mocked_response

        server_wrapper = APIServerWrapper(url="fake_url")
        self.assertEqual(server_wrapper.json, {'p1': 'a1', 'p2': 'a2'})
        self.assertEqual(server_wrapper.resp_code, 200)

    @patch('airquality.url.api_server_wrap.requests.get')
    def test_raise_bad_api_server_response_error(self, mocked_get):
        mocked_get.side_effect = [HTTPError]

        with self.assertRaises(BadAPIServerResponseError):
            APIServerWrapper(url="fake_url")


if __name__ == '__main__':
    main()
