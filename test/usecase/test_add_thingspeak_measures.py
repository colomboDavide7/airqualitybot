######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 16:30
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import test._test_utils as tutils
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.extra.timest import thingspeak_timest
from airquality.datamodel.apiparam import APIParam
from airquality.url.url_reader import URLReader
from airquality.usecase.add_station_measures import AddThingspeakMeasures


def _test_measure_param():
    """
    :return: a dict object that represents the 'param_code' -> 'param_id' mapping used for building requests.
    """
    return {'pm1.0_atm_a': 12, 'pm2.5_atm_a': 13, 'pm10.0_atm_a': 14, 'temperature_a': 15, 'humidity_a': 16}


def _test_max_station_packet_id_plus_one() -> int:
    """
    :return: the integer that represents the station max packet id plus one (returned by the DatabaseGateway).
    """
    return 140


def _test_tzinfo():
    """
    :return: the 'tzinfo' object used in this test
    """
    return tutils.get_tzinfo_from_coordinates(latitude=45, longitude=9)


def _test_sensor_api_param():
    """
    :return: return the *APIParam* used for this integration test.
    """
    return APIParam(
        sensor_id=99,
        api_key="fakekey",
        api_id="fakeid",
        ch_name="1A",
        last_acquisition=datetime(2021, 12, 20, 11, 38, tzinfo=_test_tzinfo())
    )


def _mocked_database_gway() -> MagicMock:
    """
    :return: a *MagicMock* instance that implements all the *DatabaseGateway* relevant methods for this class.
    """
    mocked_gateway = MagicMock()
    mocked_gateway.insert_station_measures = MagicMock()
    mocked_gateway.query_max_station_packet_id_plus_one.return_value = _test_max_station_packet_id_plus_one()
    mocked_gateway.query_sensor_apiparam_of_type.return_value = [_test_sensor_api_param()]
    mocked_gateway.query_measure_param_owned_by.return_value = _test_measure_param()
    mocked_gateway.query_last_acquisition_of.return_value = datetime(2021, 12, 20, 11, 18, 40, tzinfo=_test_tzinfo())
    return mocked_gateway


def _mocked_json_response() -> MagicMock:
    """
    :return: a *MagicMock* instance that implements the 'json' method of Response object in requests module.
    """
    mocked_resp = MagicMock()
    mocked_resp.json.return_value = tutils.get_json_response_from_file(filename='thingspeak_response_1A.json')
    mocked_resp.status_code = 200
    return mocked_resp


def _expected_measure_record() -> str:
    """
    :return: the test measure record according to the filtered json responses used in this test.
    """
    ts = '2021-12-20 12:18:40+01:00'
    return f"(140, 99, 12, 20.5, '{ts}')," \
           f"(140, 99, 13, 35.53, '{ts}')," \
           f"(140, 99, 14, 37.43, '{ts}')," \
           f"(140, 99, 15, 55.0, '{ts}')," \
           f"(140, 99, 16, 60.0, '{ts}')"


def _mocked_environ():
    return {
        'thingspeak_url': "fake_url",
        'logging_dir': "fake_dir"
    }


class AddThingspeakMeasuresIntegrationTest(TestCase):
    """
    A class that defines the integration test for *AddThingspeakMeasures* usecase.
    """

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._mocked_database_gway = _mocked_database_gway()
        self._usecase = AddThingspeakMeasures(
            database_gway=self._mocked_database_gway,
            timest=thingspeak_timest(),
            url_reader=URLReader()
        )

# =========== TEST METHODS
    @patch('airquality.extra.logger_extra.logging')
    @patch('airquality.environment.os')
    @patch('airquality.url.url_reader.requests.get')
    def test_add_thingspeak_measures_usecase(self, mocked_get, mocked_os, mocked_logging):
        mocked_os.environ = _mocked_environ()
        mocked_get.return_value = _mocked_json_response()
        self._usecase.run()
        self._assert_responses()
        self._assert_usecase_properties()

# =========== SUPPORT METHODS
    def _assert_responses(self):
        responses = self._mocked_database_gway.insert_station_measures.call_args[1]['responses']
        self.assertEqual(len(responses), 3)
        self.assertEqual(responses[0].measure_record, _expected_measure_record())

    def _assert_usecase_properties(self):
        self.assertEqual(self._usecase._packet_id(), 140)
        self.assertEqual(self._usecase._database_api_param(), [_test_sensor_api_param()])
        self.assertEqual(self._usecase._database_measure_param(), _test_measure_param())


if __name__ == '__main__':
    main()
