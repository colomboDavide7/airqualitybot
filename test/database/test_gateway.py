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
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.response import AddOpenWeatherMapDataResponse


class MockedDatabaseAdapter(MagicMock):

    def __repr__(self):
        return "mocked database adapter"


class TestDatabaseGateway(TestCase):

    ##################################### test_update_last_acquisition #####################################
    def test_update_last_acquisition(self):
        mocked_database_adapter = MockedDatabaseAdapter()
        mocked_database_adapter.execute = MagicMock()

        gateway = DatabaseGateway(database_adapt=mocked_database_adapter)
        gateway.update_last_acquisition_of(timestamp="faketimestamp", sensor_id=12, ch_name="fakename")

        expected_query = "UPDATE level0_raw.sensor_api_param SET last_acquisition = 'faketimestamp' " \
                         "WHERE sensor_id = 12 AND ch_name = 'fakename';"

        mocked_database_adapter.execute.assert_called_with(expected_query)

    ##################################### test_update_last_acquisition #####################################
    def test_get_apiparam_of_type(self):
        test_last_acquisition = datetime.strptime("2018-12-11 09:59:00", "%Y-%m-%d %H:%M:%S")
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchall.side_effect = [
            [(1, 'k1', 'i1', 'n1', test_last_acquisition),
             (1, 'k2', 'i2', 'n2', test_last_acquisition),
             (2, 'z1', 'a1', 'm1', test_last_acquisition)],
            []]

        gateway = DatabaseGateway(database_adapt=mocked_dbadapter)
        actual = gateway.get_sensor_apiparam_of_type(sensor_type="faketype")
        self.assertEqual(len(actual), 3)

        expected_apiparam = [
            APIParam(sensor_id=1, api_key="k1", api_id="i1", ch_name="n1", last_acquisition=test_last_acquisition),
            APIParam(sensor_id=1, api_key="k2", api_id="i2", ch_name="n2", last_acquisition=test_last_acquisition),
            APIParam(sensor_id=2, api_key="z1", api_id="a1", ch_name="m1", last_acquisition=test_last_acquisition)
        ]
        self.assertEqual(actual, expected_apiparam)

        with self.assertRaises(ValueError):
            gateway.get_sensor_apiparam_of_type(sensor_type="faketype")

    ##################################### test_get_max_mobile_packet_id_plus_one #####################################
    def test_get_last_acquisition_timestamp_of_sensor_channel(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchone.return_value = (datetime.strptime("2012-09-17 08:37:00", "%Y-%m-%d %H:%M:%S"),)

        actual = DatabaseGateway(database_adapt=mocked_dbadapter).get_last_acquisition_of(sensor_id=12,
                                                                                          ch_name="fakename")
        self.assertEqual(actual, datetime.strptime("2012-09-17 08:37:00", "%Y-%m-%d %H:%M:%S"))

    ##################################### test_get_max_station_packet_id_plus_one #####################################
    def test_get_service_id_from_service_name(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchone.side_effect = [(1,), None]

        gateway = DatabaseGateway(database_adapt=mocked_dbadapter)
        actual = gateway.get_service_id_from_name(service_name="fakename")
        self.assertEqual(actual, 1)

        with self.assertRaises(ValueError):
            gateway.get_service_id_from_name(service_name="fakename")

    ##################################### test_get_service_apiparam #####################################
    def test_get_service_apiparam(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchall.side_effect = [[('key1', 0), ('key2', 12)], []]

        gateway = DatabaseGateway(database_adapt=mocked_dbadapter)
        actual = gateway.get_service_apiparam_of(service_name="fakename")
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].api_key, "key1")
        self.assertEqual(actual[0].n_requests, 0)
        self.assertEqual(actual[1].api_key, "key2")
        self.assertEqual(actual[1].n_requests, 12)

        with self.assertRaises(ValueError):
            gateway.get_service_apiparam_of(service_name="fakename")

    ##################################### test_get_weather_condition #####################################
    def test_get_weather_condition(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.fetchall.side_effect = [
            [(55, 804, "04d"),
             (37, 500, "13d"),
             (56, 804, "04n")],
            []]

        gateway = DatabaseGateway(database_adapt=mocked_dbadapter)
        actual = gateway.get_weather_conditions()
        self.assertEqual(len(actual), 3)

        expected_output = [(55, 804, "04d"),
                           (37, 500, "13d"),
                           (56, 804, "04n")]
        self.assertEqual(actual, expected_output)

        with self.assertRaises(ValueError):
            gateway.get_weather_conditions()

    @property
    def get_test_add_weather_data_response(self):
        return AddOpenWeatherMapDataResponse(
            current_weather_record="(1, 14400, 55, 8.84, 1018, 81, 0.59, 106, NULL, NULL, '2022-01-03 14:47:11')",
            hourly_forecast_record="(1, 14400, 55, 9.21, 1018, 80, 0.33, 186, 0.21, NULL, '2022-01-03 14:00:00')",
            daily_forecast_record="(1, 14400, 55, 9.25, 5.81, 9.4, 1019, 83, 2.72, 79, NULL, NULL, '2022-01-03 12:00:00')"
        )

    ##################################### test_insert_weather_data #####################################
    def test_insert_weather_data(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.execute = MagicMock()

        mocked_response_builder = MagicMock()
        mocked_response_builder.__len__.return_value = 1
        mocked_response_builder.__iter__.return_value = [self.get_test_add_weather_data_response]

        DatabaseGateway(database_adapt=mocked_dbadapter).insert_weather_data(responses=mocked_response_builder)

        expected_query = \
            "INSERT INTO level0_raw.current_weather (service_id, geoarea_id, weather_id, temperature, pressure, " \
            "humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES " \
            "(1, 14400, 55, 8.84, 1018, 81, 0.59, 106, NULL, NULL, '2022-01-03 14:47:11'); " \
            "INSERT INTO level0_raw.hourly_forecast (service_id, geoarea_id, weather_id, temperature, pressure, " \
            "humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES " \
            "(1, 14400, 55, 9.21, 1018, 80, 0.33, 186, 0.21, NULL, '2022-01-03 14:00:00'); " \
            "INSERT INTO level0_raw.daily_forecast (service_id, geoarea_id, weather_id, temperature, min_temp, max_temp, " \
            "pressure, humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES " \
            "(1, 14400, 55, 9.25, 5.81, 9.4, 1019, 83, 2.72, 79, NULL, NULL, '2022-01-03 12:00:00');"

        mocked_dbadapter.execute.assert_called_with(expected_query)

    def test_delete_all_from_hourly_weather_forecast(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.execute = MagicMock()

        DatabaseGateway(database_adapt=mocked_dbadapter).delete_all_from_hourly_weather_forecast()
        expected_query = "DELETE FROM level0_raw.hourly_forecast;"
        mocked_dbadapter.execute.assert_called_with(expected_query)

    def test_delete_all_from_daily_weather_forecast(self):
        mocked_dbadapter = MockedDatabaseAdapter()
        mocked_dbadapter.execute = MagicMock()

        DatabaseGateway(database_adapt=mocked_dbadapter).delete_all_from_daily_weather_forecast()
        expected_query = "DELETE FROM level0_raw.daily_forecast;"
        mocked_dbadapter.execute.assert_called_with(expected_query)


if __name__ == '__main__':
    main()
