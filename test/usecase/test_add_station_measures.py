######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 16:30
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.datamodel.apiparam import APIParam
from airquality.usecase.add_station_measures import AddThingspeakMeasures


class TestAddStationMeasures(TestCase):

    @property
    def get_test_measure_param(self):
        return {'pm1.0_atm_a': 12, 'pm2.5_atm_a': 13, 'pm10.0_atm_a': 14, 'temperature_a': 15, 'humidity_a': 16}

    @property
    def get_test_apiparam(self):
        test_last_acquisition = datetime.strptime('2021-12-20 10:38:00', '%Y-%m-%d %H:%M:%S')
        return APIParam(sensor_id=99, api_key="fakekey", api_id="fakeid", ch_name="1A", last_acquisition=test_last_acquisition)

    @patch('airquality.core.apidata_builder.urlopen')
    @patch('airquality.url.timeiter_url.datetime')
    def test_add_station_measures(self, mocked_datetime, mocked_urlopen):
        mocked_datetime.now.return_value = datetime.strptime('2021-12-20 17:12:00', '%Y-%m-%d %H:%M:%S')

        with open('test_resources/thingspeak_response_1A.json', 'r') as f:
            apiresp = f.read()

        mocked_apiresp = MagicMock()
        mocked_apiresp.read.return_value = apiresp
        mocked_apiresp.__enter__.return_value = mocked_apiresp
        mocked_urlopen.return_value = mocked_apiresp

        mocked_gateway = MagicMock()
        mocked_gateway.insert_station_measures = MagicMock()
        mocked_gateway.get_max_station_packet_id_plus_one.return_value = 140
        mocked_gateway.get_sensor_apiparam_of_type.return_value = [self.get_test_apiparam]
        mocked_gateway.get_measure_param_owned_by.return_value = self.get_test_measure_param
        mocked_gateway.get_last_acquisition_of_sensor_channel.return_value = datetime.strptime('2021-12-20 11:17:40', '%Y-%m-%d %H:%M:%S')

        use_case = AddThingspeakMeasures(output_gateway=mocked_gateway, input_url_template="fakeurl")
        self.assertEqual(use_case.api_param, [self.get_test_apiparam])
        self.assertEqual(use_case.start_packet_id, 140)
        self.assertEqual(use_case.measure_param, self.get_test_measure_param)

        use_case.run()
        responses = mocked_gateway.insert_station_measures.call_args[1]['responses']
        self.assertEqual(len(responses), 3)

        resp = responses[0]
        expected_measure_record = "(140, 99, 12, 20.5, '2021-12-20 11:18:40'),(140, 99, 13, 35.53, '2021-12-20 11:18:40')," \
                                  "(140, 99, 14, 37.43, '2021-12-20 11:18:40'),(140, 99, 15, 55.0, '2021-12-20 11:18:40')," \
                                  "(140, 99, 16, 60.0, '2021-12-20 11:18:40')"
        self.assertEqual(resp.measure_record, expected_measure_record)


if __name__ == '__main__':
    main()
