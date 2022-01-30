# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 20:09
# ======================================
from unittest import TestCase, main
from unittest.mock import patch, MagicMock

import requests

from airquality.url.url_reader import json_http_response


def _test_status_code():
    return 200


def _test_json_response():
    return b'{"p1": "a1", "p2": "a2"}'


def _mocked_json_response() -> MagicMock:
    mocked_response = MagicMock()
    mocked_response.content = _test_json_response()
    mocked_response.status_code = _test_status_code()
    return mocked_response


def _mocked_http_bad_response() -> MagicMock:
    mocked_r = MagicMock()
    mocked_r.content = _test_json_response()
    mocked_r.status_code = 400
    return mocked_r


class TestURLReader(TestCase):

# =========== TEST METHODS
    @patch('airquality.url.url_reader.requests.get')
    def test_successfully_get_response_from_server(self, mocked_get):
        mocked_get.return_value = _mocked_json_response()
        actual_jresp = json_http_response(url='fake url')
        self.assertEqual(
            actual_jresp,
            {"p1": "a1", "p2": "a2"}
        )

    @patch('airquality.url.url_reader.requests.get')
    def test_raise_bad_api_server_response_error(self, mocked_get):
        mocked_get.return_value = _mocked_http_bad_response()
        with self.assertRaises(requests.HTTPError):
            json_http_response(url='fake url')


if __name__ == '__main__':
    main()
