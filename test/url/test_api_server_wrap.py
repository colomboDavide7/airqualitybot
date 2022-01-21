# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 20:09
# ======================================
from unittest import TestCase, main
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError
from airquality.url.api_server_wrap import APIServerWrapper, BadAPIServerResponseError


def _test_status_code():
    return 200


def _test_json_response():
    return {'p1': 'a1', 'p2': 'a2'}


def _mocked_json_response() -> MagicMock:
    mocked_response = MagicMock()
    mocked_response.json.return_value = _test_json_response()
    mocked_response.status_code = _test_status_code()
    return mocked_response


class TestAPIServerWrapper(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self.server_wrap = APIServerWrapper(timeout=5.0)

# =========== TEST METHODS
    @patch('airquality.url.api_server_wrap.requests.get')
    def test_successfully_get_response_from_server(self, mocked_get):
        mocked_get.return_value = _mocked_json_response()
        actual_jresp = self.server_wrap.json(url="fake_url")
        self.assertEqual(actual_jresp, _test_json_response())

    @patch('airquality.url.api_server_wrap.requests.get')
    def test_raise_bad_api_server_response_error(self, mocked_get):
        mocked_get.side_effect = [HTTPError]
        with self.assertRaises(BadAPIServerResponseError):
            self.server_wrap.json(url="fake_url")


if __name__ == '__main__':
    main()
