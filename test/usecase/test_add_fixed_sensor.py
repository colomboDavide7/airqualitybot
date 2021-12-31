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
from airquality.datamodel.apidata import PurpleairAPIData
from airquality.usecase.add_fixed_sensors import AddFixedSensors


class TestAddFixedSensor(TestCase):

    @property
    def get_test_purpleair_datamodel(self):
        return PurpleairAPIData(
            name="fakename",
            sensor_index=9,
            latitude=1.234,
            longitude=5.666,
            altitude=0,
            primary_id_a=111,
            primary_key_a="key1a",
            primary_id_b=222,
            primary_key_b="key1b",
            secondary_id_a=333,
            secondary_key_a="key2a",
            secondary_id_b=444,
            secondary_key_b="key2b",
            date_created=1234567890
        )

    @property
    def get_expected_apiparam(self):
        return "(1, 'key1a', '111', '1A', '2009-02-14 00:31:30'),(1, 'key1b', '222', '1B', '2009-02-14 00:31:30')," \
               "(1, 'key2a', '333', '2A', '2009-02-14 00:31:30'),(1, 'key2b', '444', '2B', '2009-02-14 00:31:30')"

    @patch('airquality.response_builder.datetime')
    def test_add_fixed_sensor_use_case(self, mocked_datetime):
        mocked_now = datetime.strptime("2021-12-29 18:33:00", "%Y-%m-%d %H:%M:%S")
        mocked_datetime.now.return_value = mocked_now

        mocked_datamodel = MagicMock()
        mocked_datamodel.__len__.return_value = 1
        mocked_datamodel.__iter__.return_value = [self.get_test_purpleair_datamodel]

        mocked_database_gateway = MagicMock()
        mocked_database_gateway.insert_sensors = MagicMock()

        AddFixedSensors(output_gateway=mocked_database_gateway, existing_names=set(), start_sensor_id=1).process(datamodels=mocked_datamodel)

        responses = mocked_database_gateway.insert_sensors.call_args[1]['responses']
        self.assertEqual(len(responses), 1)

        resp = responses[0]
        self.assertEqual(resp.sensor_record, "(1, 'Purpleair/Thingspeak', 'fakename (9)')")
        self.assertEqual(resp.apiparam_record, self.get_expected_apiparam)
        self.assertEqual(resp.geolocation_record, "(1, '2021-12-29 18:33:00', ST_GeomFromText('POINT(5.666 1.234)', 26918))")


if __name__ == '__main__':
    main()
