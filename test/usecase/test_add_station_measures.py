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
from airquality.datamodel.timest import thingspeak_timest
from airquality.datamodel.apiparam import APIParam
from airquality.url.api_server_wrap import APIServerWrapper
from airquality.usecase.add_station_measures import AddThingspeakMeasures


class AddThingspeakMeasuresIntegrationTest(TestCase):
    """
    A class that defines the integration test for *AddThingspeakMeasures* usecase.
    """

# =========== TEST METHODS
    @patch('airquality.url.api_server_wrap.requests.get')
    def test_add_thingspeak_measures_usecase(self, mocked_get):
        mocked_get.return_value = self.mocked_api_response
        mocked_gateway = self.mocked_database_gway

        # TODO: add Timest reference !!!!
        usecase = AddThingspeakMeasures(
            database_gway=mocked_gateway,
            timest=thingspeak_timest(),
            server_wrap=APIServerWrapper(),
            input_url_template="fakeurl"
        )

        usecase.run()
        responses = mocked_gateway.insert_station_measures.call_args[1]['responses']
        self.assertEqual(len(responses), 3)
        self.assertEqual(usecase.start_packet_id, 140)
        self.assertEqual(usecase.api_param, [self.get_test_apiparam])
        self.assertEqual(usecase.measure_param, self.get_test_measure_param)
        self.assertEqual(responses[0].measure_record, self.get_expected_measure_record)

# =========== SUPPORT METHODS
    @property
    def get_test_measure_param(self):
        """
        :return: a dict object that represents the 'param_code' -> 'param_id' mapping used for building requests.
        """
        return {'pm1.0_atm_a': 12, 'pm2.5_atm_a': 13, 'pm10.0_atm_a': 14, 'temperature_a': 15, 'humidity_a': 16}

    @property
    def get_test_apiparam(self):
        """
        :return: return the *APIParam* used for this integration test.
        """
        return APIParam(
            sensor_id=99,
            api_key="fakekey",
            api_id="fakeid",
            ch_name="1A",
            last_acquisition=datetime(2021, 12, 20, 11, 38, tzinfo=self.get_test_tzinfo)
        )

    @property
    def get_test_station_packet_id(self) -> int:
        """
        :return: the integer that represents the station max packet id plus one (returned by the DatabaseGateway).
        """
        return 140

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
        mocked_resp.json.return_value = tutils.get_json_response_from_file(filename='thingspeak_response_1A.json')
        return mocked_resp

    @property
    def mocked_database_gway(self) -> MagicMock:
        """
        :return: a *MagicMock* instance that implements all the *DatabaseGateway* relevant methods for this class.
        """
        mocked_gateway = MagicMock()
        mocked_gateway.insert_station_measures = MagicMock()
        mocked_gateway.get_max_station_packet_id_plus_one.return_value = self.get_test_station_packet_id
        mocked_gateway.get_sensor_apiparam_of_type.return_value = [self.get_test_apiparam]
        mocked_gateway.get_measure_param_owned_by.return_value = self.get_test_measure_param
        mocked_gateway.get_last_acquisition_of.return_value = \
            datetime(2021, 12, 20, 11, 18, 40, tzinfo=self.get_test_tzinfo)
        return mocked_gateway

    @property
    def get_expected_measure_record(self) -> str:
        """
        :return: the test measure record according to the filtered json responses used in this test.
        """
        ts = '2021-12-20 12:18:40+01:00'
        return f"(140, 99, 12, 20.5, '{ts}')," \
               f"(140, 99, 13, 35.53, '{ts}')," \
               f"(140, 99, 14, 37.43, '{ts}')," \
               f"(140, 99, 15, 55.0, '{ts}')," \
               f"(140, 99, 16, 60.0, '{ts}')"


if __name__ == '__main__':
    main()
