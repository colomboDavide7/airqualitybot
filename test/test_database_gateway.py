######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 14:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.response import AddFixedSensorResponse
from airquality.database_gateway import DatabaseGateway


class TestDatabaseGateway(TestCase):

    @property
    def get_test_existing_names(self):
        return [("n1", ), ("n2", ), ("n3", )]

    def test_get_existing_sensor_names(self):
        mocked_dbadapter = MagicMock()
        mocked_dbadapter.fetchall.return_value = [("n1", ), ("n2", ), ("n3", )]

        gateway = DatabaseGateway(dbadapter=mocked_dbadapter)

        existing_sensor_names = gateway.get_existing_sensor_names_of_type(sensor_type="purpleair")
        self.assertEqual(existing_sensor_names, {"n1", "n2", "n3"})

    def test_get_start_sensor_id(self):
        mocked_dbadapter = MagicMock()
        mocked_dbadapter.fetchone.side_effect = [(12, ), None]
        gateway = DatabaseGateway(dbadapter=mocked_dbadapter)
        start_sensor_id = gateway.get_start_sensor_id()
        self.assertEqual(start_sensor_id, 13)

        start_sensor_id = gateway.get_start_sensor_id()
        self.assertEqual(start_sensor_id, 1)

    @property
    def get_test_sensor_record(self):
        return "(12, 'faketype', 'fakename')"

    @property
    def get_test_apiparam_record(self):
        return "(12, 'key1', 'ident1', 'name1', '2018-12-13 18:19:00'),(12, 'key2', 'ident2', 'name2', '2018-12-13 18:19:00')"

    @property
    def get_test_geolocation_record(self):
        return "(12, '2019-09-25 17:44:00', NULL, ST_GeomFromText('POINT(-9 36)', 26918))"

    @property
    def get_test_add_fixed_sensor_responses(self):
        return AddFixedSensorResponse(
            sensor_record=self.get_test_sensor_record,
            apiparam_record=self.get_test_apiparam_record,
            geolocation_record=self.get_test_geolocation_record
        )

    def test_insert_sensors(self):
        mocked_database_adapter = MagicMock()
        mocked_database_adapter.execute = MagicMock()

        mocked_response_builder = MagicMock()
        mocked_response_builder.__iter__.return_value = [self.get_test_add_fixed_sensor_responses]
        gateway = DatabaseGateway(dbadapter=mocked_database_adapter)
        gateway.insert_sensors(responses=mocked_response_builder)

        expected_query = \
            "INSERT INTO level0_raw.sensor VALUES (12, 'faketype', 'fakename'); " \
            "INSERT INTO level0_raw.sensor_api_param (sensor_id, ch_key, ch_id, ch_name, last_acquisition) VALUES " \
            "(12, 'key1', 'ident1', 'name1', '2018-12-13 18:19:00'),(12, 'key2', 'ident2', 'name2', '2018-12-13 18:19:00'); " \
            "INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) VALUES " \
            "(12, '2019-09-25 17:44:00', NULL, ST_GeomFromText('POINT(-9 36)', 26918));"

        mocked_database_adapter.execute.assert_called_with(expected_query)


if __name__ == '__main__':
    main()
