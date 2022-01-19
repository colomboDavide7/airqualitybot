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
from airquality.usecase.add_fixed_sensors import AddPurpleairFixedSensors


class TestAddFixedSensor(TestCase):

    @patch('airquality.core.response_builder.datetime')
    @patch('airquality.url.api_server_wrap.requests.get')
    def test_add_fixed_sensors_usecase(self, mocked_get, mocked_datetime):
        mocked_now = datetime.strptime("2021-12-29 18:33:00", "%Y-%m-%d %H:%M:%S")
        mocked_datetime.now.return_value = mocked_now

        test_json_response = tutils.get_json_response_from_file(filename='purpleair_response.json')
        mocked_resp = MagicMock()
        mocked_resp.json.return_value = test_json_response
        mocked_resp.status_code = 200
        mocked_get.return_value = mocked_resp

        mocked_gateway = MagicMock()
        mocked_gateway.get_max_sensor_id_plus_one.return_value = 1
        mocked_gateway.get_existing_sensor_names_of_type.return_value = {'n1 (1)', 'n2 (2)'}
        mocked_gateway.insert_sensors = MagicMock()

        use_case = AddPurpleairFixedSensors(output_gateway=mocked_gateway, input_url_template="fake_url")

        self.assertEqual(use_case.start_sensor_id, 1)
        self.assertEqual(len(use_case.names_of), 2)
        self.assertIn('n1 (1)', use_case.names_of)
        self.assertIn('n2 (2)', use_case.names_of)

        use_case.run()
        responses = mocked_gateway.insert_sensors.call_args[1]['responses']
        self.assertEqual(len(responses), 1)
        resp = responses[0]
        self.assertEqual(resp.sensor_record, "(1, 'Purpleair/Thingspeak', 'n3 (3)')")
        self.assertEqual(resp.apiparam_record, self.get_expected_apiparam)
        self.assertEqual(resp.geolocation_record,
                         "(1, '2021-12-29 18:33:00', ST_GeomFromText('POINT(9.12 45.24)', 4326))")

    @property
    def get_expected_apiparam(self):
        return "(1, 'key1a3', '119', '1A', '2018-09-29 23:10:23'),(1, 'key1b3', '120', '1B', '2018-09-29 23:10:23')," \
               "(1, 'key2a3', '121', '2A', '2018-09-29 23:10:23'),(1, 'key2b3', '122', '2B', '2018-09-29 23:10:23')"


if __name__ == '__main__':
    main()
