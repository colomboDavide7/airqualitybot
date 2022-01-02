######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 20:21
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.request import AddFixedSensorsRequest, Channel
from airquality.usecase.add_fixed_sensors import AddFixedSensors


class TestAddFixedSensor(TestCase):

    @property
    def get_test_geolocation(self):
        return PostgisPoint(latitude=1.234, longitude=5.666)

    @property
    def get_test_channels(self):
        test_last_acquisition = datetime.fromtimestamp(1234567890)
        return [
            Channel(api_key="key1a", api_id="111", channel_name="1A", last_acquisition=test_last_acquisition),
            Channel(api_key="key1b", api_id="222", channel_name="1B", last_acquisition=test_last_acquisition),
            Channel(api_key="key2a", api_id="333", channel_name="2A", last_acquisition=test_last_acquisition),
            Channel(api_key="key2b", api_id="444", channel_name="2B", last_acquisition=test_last_acquisition)
        ]

    @property
    def get_test_purpleair_request(self):
        return AddFixedSensorsRequest(
            name="fakename (9)",
            type="Purpleair/Thingspeak",
            channels=self.get_test_channels,
            geolocation=self.get_test_geolocation
        )

    @property
    def get_expected_apiparam(self):
        return "(1, 'key1a', '111', '1A', '2009-02-14 00:31:30'),(1, 'key1b', '222', '1B', '2009-02-14 00:31:30')," \
               "(1, 'key2a', '333', '2A', '2009-02-14 00:31:30'),(1, 'key2b', '444', '2B', '2009-02-14 00:31:30')"

    @patch('airquality.core.response_builder.datetime')
    def test_add_fixed_sensor_use_case(self, mocked_datetime):
        mocked_now = datetime.strptime("2021-12-29 18:33:00", "%Y-%m-%d %H:%M:%S")
        mocked_datetime.now.return_value = mocked_now

        mocked_request_builder = MagicMock()
        mocked_request_builder.__len__.return_value = 1
        mocked_request_builder.__iter__.return_value = [self.get_test_purpleair_request]

        mocked_database_gateway = MagicMock()
        mocked_database_gateway.insert_sensors = MagicMock()

        AddFixedSensors(
            output_gateway=mocked_database_gateway, existing_names=set(), start_sensor_id=1
        ).process(requests=mocked_request_builder)

        responses = mocked_database_gateway.insert_sensors.call_args[1]['responses']
        self.assertEqual(len(responses), 1)

        resp = responses[0]
        self.assertEqual(resp.sensor_record, "(1, 'Purpleair/Thingspeak', 'fakename (9)')")
        self.assertEqual(resp.apiparam_record, self.get_expected_apiparam)
        self.assertEqual(resp.geolocation_record, "(1, '2021-12-29 18:33:00', ST_GeomFromText('POINT(5.666 1.234)', 26918))")


if __name__ == '__main__':
    main()
