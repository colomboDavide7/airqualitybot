######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 14:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.apidata import WeatherCityData
from airquality.datamodel.apiparam import APIParam
from airquality.datamodel.response import AddFixedSensorResponse, AddMobileMeasureResponse, AddStationMeasuresResponse, \
    AddPlacesResponse
from airquality.database.gateway import DatabaseGateway


class MockedDatabaseAdapter(MagicMock):

    def __repr__(self):
        return "mocked database adapter"


class TestDatabaseGateway(TestCase):

    ##################################### test_get_existing_sensor_names #####################################
    def test_get_existing_sensor_names(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchall.return_value = [("n1", ), ("n2", ), ("n3", )]

        gateway = DatabaseGateway(dbadapter=mocked_dbadapter)
        self.assertEqual(repr(gateway), "DatabaseGateway(dbadapter=mocked database adapter)")

        existing_sensor_names = gateway.get_existing_sensor_names_of_type(sensor_type="purpleair")
        self.assertEqual(existing_sensor_names, {"n1", "n2", "n3"})

    ##################################### test_get_max_sensor_id_plus_one #####################################
    def test_get_max_sensor_id_plus_one(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchone.side_effect = [(12, ), (None, )]

        gateway = DatabaseGateway(dbadapter=mocked_dbadapter)
        start_sensor_id = gateway.get_max_sensor_id_plus_one()
        self.assertEqual(start_sensor_id, 13)

        start_sensor_id = gateway.get_max_sensor_id_plus_one()
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

    ##################################### test_insert_sensors #####################################
    def test_insert_sensors(self):
        mocked_database_adapter = MockedDatabaseAdapter()
        mocked_database_adapter.execute = MagicMock()

        mocked_response_builder = MagicMock()
        mocked_response_builder.__len__.return_value = 1
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

    ##################################### test_get_measure_param #####################################
    def test_get_measure_param(self):
        mocked_database_adapter = MockedDatabaseAdapter()
        mocked_database_adapter.fetchall.return_value = [(1, 'c1'), (2, 'c2')]

        gateway = DatabaseGateway(dbadapter=mocked_database_adapter)
        actual = gateway.get_measure_param_owned_by(owner="atmotube")
        expected = {'c1': 1, 'c2': 2}
        self.assertEqual(actual, expected)

    @property
    def get_test_mobile_records(self):
        return "(13, 1, '0.17', '2021-10-11 09:44:00', ST_GeomFromText('POINT(-12 37)', 26918)), " \
               "(13, 2, '8', '2021-10-11 09:44:00', ST_GeomFromText('POINT(-12.09 37.11)', 26918)), " \
               "(13, 6, '24', '2021-10-11 09:44:00', ST_GeomFromText('POINT(-12.34 37.87)', 26918))"

    @property
    def get_test_add_mobile_sensor_responses(self):
        return AddMobileMeasureResponse(measure_record=self.get_test_mobile_records)

    ##################################### test_get_measure_param #####################################
    def test_insert_mobile_sensor_measures(self):
        mocked_database_adapter = MockedDatabaseAdapter()
        mocked_database_adapter.execute = MagicMock()

        mocked_response_builder = MagicMock()
        mocked_response_builder.__iter__.return_value = [self.get_test_add_mobile_sensor_responses]

        gateway = DatabaseGateway(dbadapter=mocked_database_adapter)
        gateway.insert_mobile_sensor_measures(responses=mocked_response_builder)

        expected_query = "INSERT INTO level0_raw.mobile_measurement (packet_id, param_id, param_value, timestamp, geom) VALUES " \
                         f"{self.get_test_mobile_records};"

        mocked_database_adapter.execute.assert_called_with(expected_query)

    ##################################### test_update_last_acquisition #####################################
    def test_update_last_acquisition(self):
        mocked_database_adapter = MockedDatabaseAdapter()
        mocked_database_adapter.execute = MagicMock()

        gateway = DatabaseGateway(dbadapter=mocked_database_adapter)
        gateway.update_last_acquisition(timestamp="faketimestamp", sensor_id=12, ch_name="fakename")

        expected_query = "UPDATE level0_raw.sensor_api_param SET last_acquisition = 'faketimestamp' " \
                         "WHERE sensor_id = 12 AND ch_name = 'fakename';"

        mocked_database_adapter.execute.assert_called_with(expected_query)

    ##################################### test_update_last_acquisition #####################################
    def test_get_apiparam_of_type(self):
        test_last_acquisition = datetime.strptime("2018-12-11 09:59:00", "%Y-%m-%d %H:%M:%S")
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchall.return_value = [
            (1, 'k1', 'i1', 'n1', test_last_acquisition),
            (1, 'k2', 'i2', 'n2', test_last_acquisition),
            (2, 'z1', 'a1', 'm1', test_last_acquisition),
        ]

        gateway = DatabaseGateway(dbadapter=mocked_dbadapter)
        actual = gateway.get_apiparam_of_type(sensor_type="atmotube")
        self.assertEqual(len(actual), 3)

        expected_apiparam = [
            APIParam(sensor_id=1, api_key="k1", api_id="i1", ch_name="n1", last_acquisition=test_last_acquisition),
            APIParam(sensor_id=1, api_key="k2", api_id="i2", ch_name="n2", last_acquisition=test_last_acquisition),
            APIParam(sensor_id=2, api_key="z1", api_id="a1", ch_name="m1", last_acquisition=test_last_acquisition)
        ]
        self.assertEqual(actual, expected_apiparam)

    ##################################### test_get_max_mobile_packet_id_plus_one #####################################
    def test_get_max_mobile_packet_id_plus_one(self):

        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchone.return_value = (12399, )

        actual = DatabaseGateway(dbadapter=mocked_dbadapter).get_max_mobile_packet_id_plus_one()
        self.assertEqual(actual, 12400)

    ##################################### test_get_max_mobile_packet_id_plus_one #####################################
    def test_get_last_acquisition_timestamp_of_sensor_channel(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchone.return_value = (datetime.strptime("2012-09-17 08:37:00", "%Y-%m-%d %H:%M:%S"), )

        actual = DatabaseGateway(dbadapter=mocked_dbadapter).get_last_acquisition_of_sensor_channel(sensor_id=12, ch_name="fakename")
        self.assertEqual(actual, datetime.strptime("2012-09-17 08:37:00", "%Y-%m-%d %H:%M:%S"))

    @property
    def get_test_station_records(self):
        return "(140, 99, 12, 20.5, '2021-12-20 11:18:40'),(140, 99, 13, 35.53, '2021-12-20 11:18:40')," \
               "(140, 99, 14, 37.43, '2021-12-20 11:18:40'),(140, 99, 15, 55, '2021-12-20 11:18:40')," \
               "(140, 99, 16, 60, '2021-12-20 11:18:40')"

    @property
    def get_test_add_station_measures_response(self):
        return AddStationMeasuresResponse(
            measure_record=self.get_test_station_records
        )

    ##################################### test_insert_station_measures #####################################
    def test_insert_station_measures(self):

        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.execute = MagicMock()

        mocked_responses = MagicMock()
        mocked_responses.__iter__.return_value = [self.get_test_add_station_measures_response]

        DatabaseGateway(dbadapter=mocked_dbadapter).insert_station_measures(responses=mocked_responses)

        expected_query = "INSERT INTO level0_raw.station_measurement (packet_id, sensor_id, param_id, param_value, timestamp) VALUES " \
                         f"{self.get_test_station_records};"
        mocked_dbadapter.execute.assert_called_with(expected_query)

    ##################################### test_get_max_station_packet_id_plus_one #####################################
    def test_get_max_station_packet_id_plus_one(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchone.side_effect = [(149, ), (None, )]

        gateway = DatabaseGateway(dbadapter=mocked_dbadapter)
        actual = gateway.get_max_station_packet_id_plus_one()
        self.assertEqual(actual, 150)

        actual = gateway.get_max_station_packet_id_plus_one()
        self.assertEqual(actual, 1)

    ##################################### test_get_max_station_packet_id_plus_one #####################################
    def test_get_service_id_from_service_name(self):

        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchone.side_effect = [(1, )]

        actual = DatabaseGateway(dbadapter=mocked_dbadapter).get_service_id_from_name(service_name="fakename")
        self.assertEqual(actual, 1)

    ##################################### test_get_max_station_packet_id_plus_one #####################################
    def test_get_existing_poscodes_of_country(self):

        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchall.return_value = [("p1",), ("p2", ), ("p3", )]

        actual = DatabaseGateway(dbadapter=mocked_dbadapter).get_poscodes_of_country(country_code="fakecode")
        self.assertEqual(len(actual), 3)
        self.assertIn("p1", actual)
        self.assertIn("p2", actual)
        self.assertIn("p3", actual)

    @property
    def get_test_add_places_response(self):
        place_record = "(1, '27100', 'IT', 'Pavia', 'Pavia', 'Lombardia', ST_GeomFromText('POINT(9 45)', 4326))"
        return AddPlacesResponse(place_record=place_record)

    ##################################### test_insert_places #####################################
    def test_insert_places(self):

        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.execute = MagicMock()

        mocked_response_builder = MagicMock()
        mocked_response_builder.__len__.return_value = 1
        mocked_response_builder.__iter__.return_value = [self.get_test_add_places_response]

        DatabaseGateway(dbadapter=mocked_dbadapter).insert_places(responses=mocked_response_builder)

        expected_query = "INSERT INTO level0_raw.geographical_area " \
                         "(service_id, postal_code, country_code, place_name, province, state, geom) VALUES " \
                         "(1, '27100', 'IT', 'Pavia', 'Pavia', 'Lombardia', ST_GeomFromText('POINT(9 45)', 4326));"
        mocked_dbadapter.execute.assert_called_with(expected_query)

    ##################################### test_get_service_apiparam #####################################
    def test_get_service_apiparam(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchall.return_value = [('key1', 0), ('key2', 12)]

        actual = DatabaseGateway(dbadapter=mocked_dbadapter).get_service_apiparam_of(service_name="fakename")
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].api_key, "key1")
        self.assertEqual(actual[0].n_requests, 0)
        self.assertEqual(actual[1].api_key, "key2")
        self.assertEqual(actual[1].n_requests, 12)

    ##################################### test_get_weather_condition #####################################
    def test_get_weather_condition(self):

        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchall.return_value = [
            (55, 804, "04d"),
            (37, 500, "13d"),
            (56, 804, "04n")
        ]

        actual = DatabaseGateway(dbadapter=mocked_dbadapter).get_weather_conditions()
        self.assertEqual(len(actual), 2)

        expected_output = {804: {'04d': 55, '04n': 56}, 500: {"13d": 37}}
        self.assertEqual(actual, expected_output)

    ##################################### test_get_geolocation_of #####################################
    def test_get_geolocation_of(self):

        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchone.side_effect = [(14400, 9, 45), None]

        test_city = WeatherCityData(country_code="fakecode", place_name="fakename")
        gateway = DatabaseGateway(dbadapter=mocked_dbadapter)
        actual = gateway.get_geolocation_of(city=test_city)
        self.assertEqual(actual.geoarea_id, 14400)
        self.assertEqual(actual.longitude, 9)
        self.assertEqual(actual.latitude, 45)

        with self.assertRaises(ValueError):
            gateway.get_geolocation_of(city=test_city)


if __name__ == '__main__':
    main()
