######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 11:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.datamodel.apiparam import APIParam
from airquality.usecase.add_mobile_measures import AddAtmotubeMeasures


class TestAddMobileMeasuresUsecase(TestCase):

    @property
    def get_test_measure_param(self):
        return {'voc': 66, 'pm1': 48, 'pm25': 94, 'pm10': 2, 't': 4, 'h': 12, 'p': 39}

    @property
    def get_test_apiparam(self):
        test_last_acquisition = datetime.strptime("2021-08-10T23:59:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        return APIParam(sensor_id=12, api_key="fakekey", api_id="fakeid", ch_name="main", last_acquisition=test_last_acquisition)

    @patch('airquality.url.timeiter_url.datetime')
    @patch('airquality.core.apidata_builder.urlopen')
    def test_add_mobile_measures_usecase(self, mocked_urlopen, mocked_datetime):

        mocked_datetime.now.return_value = datetime.strptime("2021-08-11T17:59:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")

        with open('test_resources/atmotube_response.json', 'r') as f:
            apiresp = f.read()

        mocked_apiresp = MagicMock()
        mocked_apiresp.read.return_value = apiresp
        mocked_apiresp.__enter__.return_value = mocked_apiresp
        mocked_urlopen.return_value = mocked_apiresp

        mocked_gateway = MagicMock()
        mocked_gateway.get_measure_param_owned_by.return_value = self.get_test_measure_param
        mocked_gateway.get_max_mobile_packet_id_plus_one.return_value = 12399
        mocked_gateway.get_apiparam_of_type.return_value = [self.get_test_apiparam]
        test_filter_timestamp = datetime.strptime("2021-08-10T23:59:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        mocked_gateway.get_last_acquisition_of_sensor_channel.return_value = test_filter_timestamp
        mocked_gateway.insert_mobile_sensor_measures = MagicMock()

        use_case = AddAtmotubeMeasures(output_gateway=mocked_gateway, input_url_template="fakeurl")
        self.assertEqual(use_case.measure_param, self.get_test_measure_param)
        self.assertEqual(use_case.api_param, [self.get_test_apiparam])

        use_case.run()
        responses = mocked_gateway.insert_mobile_sensor_measures.call_args[1]['responses']
        self.assertEqual(len(responses), 1)

        resp = responses[0]
        expected_timestamp = "2021-08-11 00:00:00"
        expected_geom = "ST_GeomFromText('POINT(9 45)', 4326)"
        expected_measure_record = f"(12399, 66, 0.17, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 48, 7, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 94, 9, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 2, 10, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 4, 29, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 12, 42, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 39, 1004.72, '{expected_timestamp}', {expected_geom})"

        self.assertEqual(resp.measure_record, expected_measure_record)


if __name__ == '__main__':
    main()
