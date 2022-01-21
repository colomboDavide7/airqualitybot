######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 20:21
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import test._test_utils as tutils
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.datamodel.timest import purpleair_timest
from airquality.url.api_server_wrap import APIServerWrapper
from airquality.usecase.add_fixed_sensors import AddPurpleairFixedSensors


def _test_timezone():
    return tutils.get_tzinfo_from_coordinates(latitude=45, longitude=9)


def _mocked_datetime_utcfromtimestamp() -> MagicMock:
    mocked_utcfrom = MagicMock()
    mocked_utcfrom.return_value = datetime(2018, 9, 29, 21, 10, 23, tzinfo=_test_timezone())
    return mocked_utcfrom


def _mocked_datetime_now() -> MagicMock:
    mocked_now = MagicMock()
    mocked_now.return_value = datetime(2021, 12, 29, 19, 33, tzinfo=_test_timezone())
    return mocked_now


def _setup_mocked_json_response() -> MagicMock:
    test_json_response = tutils.get_json_response_from_file(filename='purpleair_response.json')
    mocked_resp = MagicMock()
    mocked_resp.json.return_value = test_json_response
    mocked_resp.status_code = 200
    return mocked_resp


def _expected_apiparam_record() -> str:
    ts = '2018-09-29 23:10:23+02:00'
    return f"(1, 'key1a3', '119', '1A', '{ts}')," \
           f"(1, 'key1b3', '120', '1B', '{ts}')," \
           f"(1, 'key2a3', '121', '2A', '{ts}')," \
           f"(1, 'key2b3', '122', '2B', '{ts}')"


def _expected_sensor_record() -> str:
    return "(1, 'Purpleair/Thingspeak', 'n3 (3)')"


def _expected_sensor_at_location_record() -> str:
    return "(1, '2021-12-29 19:33:00+01:00', ST_GeomFromText('POINT(9.12 45.24)', 4326))"


def _test_existing_sensor_names():
    return {'n1 (1)', 'n2 (2)'}


def _test_max_sensor_id_plus_one() -> int:
    return 1


def _setup_mocked_database_gway() -> MagicMock:
    mocked_gateway = MagicMock()
    mocked_gateway.get_max_sensor_id_plus_one.return_value = _test_max_sensor_id_plus_one()
    mocked_gateway.query_sensor_names_of_type.return_value = _test_existing_sensor_names()
    mocked_gateway.insert_sensors = MagicMock()
    return mocked_gateway


class AddPurpleairFixedSensorsIntegrationTest(TestCase):
    """
    A class that defines the integration tests for asserting the right behavior of *AddPurpleairFixedSensors* usecase.
    """

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._mocked_database_gway = _setup_mocked_database_gway()
        self._usecase = AddPurpleairFixedSensors(
            database_gway=self._mocked_database_gway,
            server_wrap=APIServerWrapper(),
            timest=purpleair_timest(),
            input_url_template="fake_url"
        )

# =========== TEST METHODS
    @patch('airquality.datamodel.timest.datetime')
    @patch('airquality.url.api_server_wrap.requests.get')
    def test_add_fixed_sensors_usecase(self, mocked_get, mocked_datetime):
        mocked_get.return_value = _setup_mocked_json_response()
        mocked_datetime.now = _mocked_datetime_now()
        mocked_datetime.utcfromtimestamp = _mocked_datetime_utcfromtimestamp()
        self._usecase.run()
        self._assert_responses()
        self._assert_usecase_properties()

# =========== SUPPORT METHODS
    def _assert_responses(self):
        responses = self._mocked_database_gway.insert_sensors.call_args[1]['responses']
        self.assertEqual(len(responses), 1)
        actual_response = responses[0]
        self.assertEqual(actual_response.sensor_record, _expected_sensor_record())
        self.assertEqual(actual_response.apiparam_record, _expected_apiparam_record())
        self.assertEqual(actual_response.geolocation_record, _expected_sensor_at_location_record())

    def _assert_usecase_properties(self,):
        self.assertEqual(self._usecase.start_sensor_id, 1)
        self.assertEqual(len(self._usecase.names_of), 2)
        self.assertIn('n1 (1)', self._usecase.names_of)
        self.assertIn('n2 (2)', self._usecase.names_of)


if __name__ == '__main__':
    main()
