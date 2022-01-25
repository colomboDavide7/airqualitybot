# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 20:09
# ======================================
from unittest import TestCase, main
from unittest.mock import patch, MagicMock
from airquality.url.url_reader import URLReader, URLReadError


def _test_status_code():
    return 200


def _test_json_response():
    return {'p1': 'a1', 'p2': 'a2'}


def _mocked_json_response() -> MagicMock:
    mocked_response = MagicMock()
    mocked_response.json.return_value = _test_json_response()
    mocked_response.status_code = _test_status_code()
    return mocked_response


def _mocked_http_bad_response() -> MagicMock:
    mocked_r = MagicMock()
    mocked_r.json.return_value = _test_json_response()
    mocked_r.status_code = 400
    return mocked_r


class TestURLReader(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self.url_reader = URLReader(timeout_in_seconds=5.0)

# =========== TEST METHODS
    @patch('airquality.url.url_reader.requests.get')
    def test_successfully_get_response_from_server(self, mocked_get):
        mocked_get.return_value = _mocked_json_response()
        actual_jresp = self.url_reader.json(url="fake_url")
        self.assertEqual(
            actual_jresp,
            _test_json_response()
        )

    @patch('airquality.url.url_reader.requests.get')
    def test_raise_bad_api_server_response_error(self, mocked_get):
        mocked_get.return_value = _mocked_http_bad_response()
        with self.assertRaises(URLReadError):
            self.url_reader.json(url="fake_url")


if __name__ == '__main__':
    main()
