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


class AddAtmotubeMeasuresIntegrationTest(TestCase):
    """
    A class that performs the proper integration test for the *AddAtmotubeMeasures* usecase.
    """

# =========== TEST METHODS
    @patch('airquality.url.api_server_wrap.requests.get')
    def test_add_atmotube_measures_usecase(self, mocked_get):
        mocked_get.return_value = self.mocked_api_response
        mocked_database_gway = self.mocked_database_gway

        usecase = AddAtmotubeMeasures(
            database_gway=mocked_database_gway,
            server_wrap=APIServerWrapper(),
            timest=atmotube_timest(),
            input_url_template="fakeurl"
        )

        usecase.run()
        responses = mocked_database_gway.insert_mobile_measures.call_args[1]['responses']
        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0].measure_record, self.get_expected_measure_record)
        self.assertEqual(usecase.measure_param, self.get_test_measure_param)
        self.assertEqual(usecase.api_param, [self.get_test_apiparam])

# =========== SUPPORT METHODS
    @property
    def get_test_measure_param(self):
        """
        :return: a dict object that represents the 'param_code' -> 'param_id' mapping used for building requests.
        """
        return {'voc': 66, 'pm1': 48, 'pm25': 94, 'pm10': 2, 't': 4, 'h': 12, 'p': 39}

    @property
    def get_test_apiparam(self):
        """
        :return: return the *APIParam* used for this integration test.
        """
        return APIParam(
            sensor_id=12,
            api_key="fakekey",
            api_id="fakeid",
            ch_name="main",
            last_acquisition=datetime(2021, 8, 11, 1, 59, tzinfo=self.get_test_tzinfo)
        )

    @property
    def get_test_mobile_packet_id(self) -> int:
        """
        :return: the integer that represents the mobile max packet id plus one (returned by the DatabaseGateway).
        """
        return 12399

    @property
    def get_test_tzinfo(self):
        """
        :return: the 'tzinfo' object used in this test
        """
        return tutils.get_tzinfo_from_coordinates(latitude=45, longitude=9)

    @property
    def mocked_api_response(self) -> MagicMock:
        """
        :return: a *MagicMock* instance that implements the 'json' method of Response object in requests module.
        """
        mocked_resp = MagicMock()
        mocked_resp.json.return_value = tutils.get_json_response_from_file(filename='atmotube_response.json')
        return mocked_resp

    @property
    def mocked_database_gway(self) -> MagicMock:
        """
        :return: a *MagicMock* instance that implements all the *DatabaseGateway* relevant methods for this class.
        """
        mocked_gateway = MagicMock()
        mocked_gateway.get_measure_param_owned_by.return_value = self.get_test_measure_param
        mocked_gateway.get_max_mobile_packet_id_plus_one.return_value = self.get_test_mobile_packet_id
        mocked_gateway.get_sensor_apiparam_of_type.return_value = [self.get_test_apiparam]
        mocked_gateway.get_last_acquisition_of.return_value = datetime(2021, 8, 11, 1, 59, tzinfo=self.get_test_tzinfo)
        mocked_gateway.insert_mobile_measures = MagicMock()         # for getting the call args
        return mocked_gateway

    @property
    def get_expected_measure_record(self) -> str:
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


if __name__ == '__main__':
    main()
