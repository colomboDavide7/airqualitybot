######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 11:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import json
import test._test_utils as tutils
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.datamodel.fromdb import SensorApiParamDM, SensorInfoDM
from airquality.usecase.atmotube import AddAtmotubeMeasures


def _test_measure_param():
    """
    :return: a dict object that represents the 'param_code' -> 'param_id' mapping used for building requests.
    """
    return {'voc': 66, 'pm1': 48, 'pm25': 94, 'pm10': 2, 't': 4, 'h': 12, 'p': 39}


def _test_max_mobile_packet_id_plus_one() -> int:
    """
    :return: the integer that represents the mobile max packet id plus one (returned by the DatabaseGateway).
    """
    return 12399


def _test_timezone():
    """
    :return: the 'tzinfo' object used in this test
    """
    return tutils.get_tzinfo_from_coordinates(latitude=45, longitude=9)


def _test_sensor_api_param():
    """
    :return: return the *APIParam* used for this integration test.
    """
    return SensorApiParamDM(
        sensor_id=12,
        api_key="fakekey",
        api_id="fakeid",
        ch_name="main",
        last_acquisition=datetime(2021, 8, 11, 1, 59, tzinfo=_test_timezone())
    )


def _test_sensor_identity():
    return SensorInfoDM(
        sensor_id=0,
        sensor_name='test_sensor'
    )


def _mocked_database_gway() -> MagicMock:
    """
    :return: a *MagicMock* instance that implements all the *DatabaseGateway* relevant methods for this class.
    """
    mocked_gateway = MagicMock()
    mocked_gateway.query_measure_param_owned_by.return_value = _test_measure_param()
    mocked_gateway.query_max_mobile_packet_id_plus_one.return_value = _test_max_mobile_packet_id_plus_one()
    mocked_gateway.query_sensor_apiparam_of_type.return_value = [_test_sensor_api_param()]
    mocked_gateway.query_last_acquisition_of.return_value = datetime(2021, 8, 11, 1, 59, tzinfo=_test_timezone())
    mocked_gateway.execute = MagicMock()
    mocked_gateway.query_mobile_sensor_unique_info.return_value = _test_sensor_identity()
    return mocked_gateway


def _mocked_json_api_resp() -> MagicMock:
    """
    :return: a *MagicMock* instance that implements the 'json' method of Response object in requests module.
    """
    _test_json_response = tutils.get_json_response_from_file(filename='atmotube_response.json')
    mocked_resp = MagicMock()
    mocked_resp.content = json.dumps(_test_json_response).encode('utf-8')
    mocked_resp.status_code = 200
    return mocked_resp


# def _mocked_datetime_now() -> MagicMock:
#     mocked_now = MagicMock()
#     mocked_now.return_value = datetime(2021, 8, 12, 12, tzinfo=_test_timezone())
#     return mocked_now
#
#
# def _mocked_datetime_strptime() -> MagicMock:
#     mocked_strptime = MagicMock()
#     mocked_strptime.return_value = datetime(2021, 8, 11)
#     return mocked_strptime
#
#
# def _mocked_datetime_replace() -> MagicMock:
#     mocked_replace = MagicMock()
#     mocked_replace.return_value = datetime(2021, 8, 11)
#     return mocked_replace
#
#
# def _mocked_datetime_astimezone() -> MagicMock:
#     mocked_astz = MagicMock()
#     mocked_astz.return_value = datetime(2021, 8, 11, 2, tzinfo=_test_timezone())
#     return mocked_astz


def _expected_measure_record() -> str:
    """
    :return: the test measure record according to the filtered json responses used in this test.
    """
    ts = "2021-08-11 02:00:00+02:00"
    geom = "ST_GeomFromText('POINT(9 45)', 4326)"
    return f"(12399, 66, 0.17, '{ts}', {geom})," \
           f"(12399, 48, 7, '{ts}', {geom})," \
           f"(12399, 94, 9, '{ts}', {geom})," \
           f"(12399, 2, 10, '{ts}', {geom})," \
           f"(12399, 4, 29, '{ts}', {geom})," \
           f"(12399, 12, 42, '{ts}', {geom})," \
           f"(12399, 39, 1004.72, '{ts}', {geom})"


def _expected_insert_mobile_measures_query():
    return "INSERT INTO level0_raw.mobile_measurement " \
           "(packet_id, param_id, param_value, timestamp, geom) " \
           f"VALUES {_expected_measure_record()};"


def _expected_update_query():
    ts = "2021-08-11 02:00:00+02:00"
    return "UPDATE level0_raw.sensor_api_param " \
           f"SET last_acquisition = '{ts}' " \
           f"WHERE sensor_id = 12 AND " \
           f"ch_name = 'main';"


def _mocked_environ():
    return {
        'atmotube_url': 'fake_url',
        'logging_dir': 'fake_dir'
    }


class AddAtmotubeMeasuresIntegrationTest(TestCase):
    """
    A class that performs the proper integration test for the *AddAtmotubeMeasures* usecase.
    """

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._mocked_database_gway = _mocked_database_gway()
        self._usecase = AddAtmotubeMeasures(database_gway=self._mocked_database_gway)

# =========== TEST METHODS
#     @patch('airquality.extra.logger_extra.logging')
    @patch('airquality.environment.os')
    @patch('airquality.extra.url.requests.get')
    def test_add_atmotube_measures_usecase(self, mocked_get, mocked_os):
        mocked_os.environ = _mocked_environ()
        mocked_get.return_value = _mocked_json_api_resp()
        self._usecase.execute()
        self._assert_responses()
        self._assert_usecase_properties()

# =========== SUPPORT METHODS
    def _assert_responses(self):
        query = self._mocked_database_gway.execute.call_args[1]['query']
        self.assertEqual(
            query,
            f"{_expected_insert_mobile_measures_query()}{_expected_update_query()}"
        )

    def _assert_usecase_properties(self):
        self.assertEqual(self._usecase._measure_param, _test_measure_param())
        self.assertEqual(self._usecase._api_param, [_test_sensor_api_param()])


if __name__ == '__main__':
    main()
