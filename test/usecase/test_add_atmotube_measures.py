######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 11:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import test._test_utils as tutils
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.datamodel.apiparam import APIParam
from airquality.datamodel.timest import atmotube_timest
from airquality.url.api_server_wrap import APIServerWrapper
from airquality.usecase.add_mobile_measures import AddAtmotubeMeasures


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
    return APIParam(
        sensor_id=12,
        api_key="fakekey",
        api_id="fakeid",
        ch_name="main",
        last_acquisition=datetime(2021, 8, 11, 1, 59, tzinfo=_test_timezone())
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
    mocked_gateway.insert_mobile_measures = MagicMock()
    return mocked_gateway


def _mocked_json_api_resp() -> MagicMock:
    """
    :return: a *MagicMock* instance that implements the 'json' method of Response object in requests module.
    """
    mocked_resp = MagicMock()
    mocked_resp.json.return_value = tutils.get_json_response_from_file(filename='atmotube_response.json')
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


class AddAtmotubeMeasuresIntegrationTest(TestCase):
    """
    A class that performs the proper integration test for the *AddAtmotubeMeasures* usecase.
    """

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._mocked_database_gway = _mocked_database_gway()
        self._usecase = AddAtmotubeMeasures(
            database_gway=self._mocked_database_gway,
            server_wrap=APIServerWrapper(),
            timest=atmotube_timest()
        )

# =========== TEST METHODS
    @patch('airquality.environment.os')
    @patch('airquality.url.api_server_wrap.requests.get')
    def test_add_atmotube_measures_usecase(self, mocked_get, mocked_os):
        mocked_os.environ = {'atmotube_url': 'fake_url'}
        mocked_get.return_value = _mocked_json_api_resp()
        self._usecase.run()
        self._assert_responses()
        self._assert_usecase_properties()

# =========== SUPPORT METHODS
    def _assert_responses(self):
        responses = self._mocked_database_gway.insert_mobile_measures.call_args[1]['responses']
        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0].measure_record, _expected_measure_record())

    def _assert_usecase_properties(self):
        self.assertEqual(self._usecase._database_measure_param(), _test_measure_param())
        self.assertEqual(self._usecase._database_api_param(), [_test_sensor_api_param()])


if __name__ == '__main__':
    main()
