# ======================================
# @author:  Davide Colombo
# @date:    2022-01-21, ven, 11:24
# ======================================
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.response import AddOpenWeatherMapDataResponse


def _expected_delete_hourly_forecast_query():
    return "DELETE FROM level0_raw.hourly_forecast;"


def _expected_delete_daily_forecast_query():
    return "DELETE FROM level0_raw.daily_forecast;"


def _test_database_weather_conditions():
    return [
        (55, 804, "04d"),
        (37, 500, "13d"),
        (56, 804, "04n")
    ]


def _test_current_weather_record():
    return "(14400, 55, 8.84, 1018, 81, 0.59, 106, NULL, NULL, '2022-01-03 14:47:11')"


def _test_hourly_forecast_record():
    return "(14400, 55, 9.21, 1018, 80, 0.33, 186, 0.21, NULL, '2022-01-03 14:00:00')"


def _test_daily_forecast_record():
    return "(14400, 55, 9.25, 5.81, 9.4, 1019, 83, 2.72, 79, NULL, NULL, '2022-01-03 12:00:00')"


def _test_weather_alert_record():
    return "(14400, 'Fake sender', 'Fake event', " \
           "'2022-01-24 19:00:00+01:00', '2022-01-25 09:59:00+01:00', " \
           "'Fake description')"


def _test_add_weather_data_response():
    return AddOpenWeatherMapDataResponse(
        current_weather_record=_test_current_weather_record(),
        hourly_forecast_record=_test_hourly_forecast_record(),
        daily_forecast_record=_test_daily_forecast_record(),
        weather_alert_record=_test_weather_alert_record()
    )


def _mocked_response_builder() -> MagicMock:
    mocked_rb = MagicMock()
    mocked_rb.__len__.return_value = 1
    mocked_rb.__iter__.return_value = [_test_add_weather_data_response()]
    return mocked_rb


def _expected_insert_weather_data_query():
    return "INSERT INTO level0_raw.current_weather (geoarea_id, weather_id, temperature, pressure, " \
            "humidity, wind_speed, wind_direction, rain, snow, timestamp, sunrise, sunset) " \
           f"VALUES {_test_current_weather_record()};" \
            "INSERT INTO level0_raw.hourly_forecast (geoarea_id, weather_id, temperature, pressure, " \
            "humidity, wind_speed, wind_direction, rain, pop, snow, timestamp) " \
           f"VALUES {_test_hourly_forecast_record()};" \
            "INSERT INTO level0_raw.daily_forecast " \
           "(geoarea_id, weather_id, temperature, min_temp, max_temp, " \
            "pressure, humidity, wind_speed, wind_direction, rain, pop, snow, timestamp) " \
           f"VALUES {_test_daily_forecast_record()};" \
           f"INSERT INTO level0_raw.weather_alert (geoarea_id, sender_name, alert_event, alert_begin, " \
           f"alert_until, description) VALUES {_test_weather_alert_record()};"


class TestDatabaseGatewayAddWeatherDataSection(TestCase):

# =========== TEST METHODS
    def test_safe_format_insert_query(self):
        gateway = DatabaseGateway(database_adapt=MagicMock())
        self.assertEqual(
            gateway._safe_format_insert_query(query="fake query {val};", values="this is my sql value"),
            "fake query this is my sql value;"
        )

    def test_empty_query_if_values_is_empty(self):
        gateway = DatabaseGateway(database_adapt=MagicMock())
        self.assertEqual(
            gateway._safe_format_insert_query(query="fake query {val};", values=""),
            ""
        )

    def test_delete_all_from_hourly_weather_forecast(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.execute = MagicMock()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        gateway.delete_all_from_hourly_weather_forecast()
        mocked_database_adapt.execute.assert_called_with(_expected_delete_hourly_forecast_query())

    def test_delete_all_from_daily_weather_forecast(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.execute = MagicMock()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        gateway.delete_all_from_daily_weather_forecast()
        mocked_database_adapt.execute.assert_called_with(_expected_delete_daily_forecast_query())

    def test_get_weather_conditions(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = _test_database_weather_conditions()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_weather_conditions(),
            _test_database_weather_conditions()
        )

    def test_raise_value_error_when_weather_conditions_are_empty(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = []
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        with self.assertRaises(ValueError):
            gateway.query_weather_conditions()

    def test_insert_weather_data(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.execute = MagicMock()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        gateway.insert_weather_data(responses=_mocked_response_builder())
        mocked_database_adapt.execute.assert_called_with(_expected_insert_weather_data_query())


if __name__ == '__main__':
    main()
