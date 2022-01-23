######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from dateutil import tz
import test._test_utils as tutils
from unittest import TestCase, main
from unittest.mock import patch, MagicMock
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.request import AddFixedSensorsRequest, AddMobileMeasuresRequest, \
    AddSensorMeasuresRequest, Channel, AddPlacesRequest, AddWeatherForecastRequest, AddOpenWeatherMapDataRequest
from airquality.core.response_builder import AddFixedSensorResponseBuilder, AddMobileMeasureResponseBuilder, \
    AddStationMeasuresResponseBuilder, AddPlacesResponseBuilder, AddOpenWeatherMapDataResponseBuilder

SQL_TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"


class TestResponseBuilder(TestCase):

    @property
    def get_test_last_acquisition(self):
        return datetime.strptime("2021-10-11 09:44:00", SQL_TIMESTAMP_FMT)

    @property
    def get_test_geolocation(self):
        return PostgisPoint(latitude=1.234, longitude=5.666)

    @property
    def get_test_channels(self):
        return [
            Channel(api_key="key1a", api_id="111", channel_name="1A", last_acquisition=self.get_test_last_acquisition),
            Channel(api_key="key1b", api_id="222", channel_name="1B", last_acquisition=self.get_test_last_acquisition),
            Channel(api_key="key2a", api_id="333", channel_name="2A", last_acquisition=self.get_test_last_acquisition),
            Channel(api_key="key2b", api_id="444", channel_name="2B", last_acquisition=self.get_test_last_acquisition)
        ]

    @property
    def get_test_validated_requests(self):
        return AddFixedSensorsRequest(
            type="faketype",
            name="fakename",
            channels=self.get_test_channels,
            geolocation=self.get_test_geolocation
        )

    ##################################### test_create_response_to_request_of_adding_fixed_sensor #####################################
    @patch('airquality.extra.timest.datetime')
    def test_create_response_to_request_of_adding_fixed_sensor(self, mocked_datetime):
        mocked_now = datetime(2021, 12, 29, 18, 33, tzinfo=tz.tzutc())
        mocked_datetime.now.return_value = mocked_now

        mocked_validated_requests = MagicMock()
        mocked_validated_requests.__iter__.return_value = [self.get_test_validated_requests]

        responses = AddFixedSensorResponseBuilder(
            requests=mocked_validated_requests,
            start_sensor_id=12
        )
        record = responses[0]
        self.assertEqual(len(responses), 1)

        expected_datetime = "2021-10-11 09:44:00"
        expected_apiparam_record = f"(12, 'key1a', '111', '1A', '{expected_datetime}')," \
                                   f"(12, 'key1b', '222', '1B', '{expected_datetime}')," \
                                   f"(12, 'key2a', '333', '2A', '{expected_datetime}')," \
                                   f"(12, 'key2b', '444', '2B', '{expected_datetime}')"

        expected_geometry = "ST_GeomFromText('POINT(5.666 1.234)', 4326)"
        expected_geolocation_record = f"(12, '2021-12-29 19:33:00+01:00', {expected_geometry})"

        self.assertEqual(record.sensor_record, "(12, 'faketype', 'fakename')")
        self.assertEqual(record.apiparam_record, expected_apiparam_record)
        self.assertEqual(record.geolocation_record, expected_geolocation_record)

    @property
    def get_test_measure_request_timestamp(self):
        return datetime(2021, 12, 29, 19, 33, tzinfo=tz.tzlocal())
        # return datetime.strptime("2021-12-29 18:33:00", SQL_TIMESTAMP_FMT)

    @property
    def get_test_measure_request_geolocation(self):
        return PostgisPoint(latitude=45.876, longitude=9.145)

    @property
    def get_test_measure_request_measures(self):
        return [(66, 0.17), (48, 8), (94, 10), (2, 11), (4, 29), (12, 42), (39, 1004.68)]

    @property
    def get_test_add_mobile_measure_request(self):
        return AddMobileMeasuresRequest(
            timestamp=self.get_test_measure_request_timestamp,
            geolocation=self.get_test_measure_request_geolocation,
            measures=self.get_test_measure_request_measures
        )

    ##################################### test_create_response_to_request_of_adding_mobile_measure #####################################
    def test_create_response_to_request_of_adding_mobile_measure(self):
        mocked_validated_request = MagicMock()
        mocked_validated_request.__iter__.return_value = [self.get_test_add_mobile_measure_request]

        responses = AddMobileMeasureResponseBuilder(requests=mocked_validated_request, start_packet_id=12399)
        resp = responses[0]

        expected_timestamp = "2021-12-29 19:33:00+01:00"
        expected_geom = "ST_GeomFromText('POINT(9.145 45.876)', 4326)"
        expected_measure_record = f"(12399, 66, 0.17, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 48, 8, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 94, 10, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 2, 11, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 4, 29, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 12, 42, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 39, 1004.68, '{expected_timestamp}', {expected_geom})"

        self.assertEqual(resp.measure_record, expected_measure_record)

    @property
    def get_test_add_sensor_measures_requests(self):
        test_tzinfo = tutils.get_tzinfo_from_coordinates(latitude=45, longitude=9)
        return AddSensorMeasuresRequest(
            timestamp=datetime(2021, 12, 20, 12, 18, 40, tzinfo=test_tzinfo),
            measures=[(12, 20.50), (14, 37.43), (15, 55), (16, 60)]
        )

    ##################################### test_create_response_to_request_of_adding_station_measures #####################################
    def test_create_response_to_request_of_adding_station_measures(self):
        mocked_valid_requests = MagicMock()
        mocked_valid_requests.__iter__.return_value = [self.get_test_add_sensor_measures_requests]

        responses = AddStationMeasuresResponseBuilder(
            requests=mocked_valid_requests,
            start_packet_id=140,
            sensor_id=99
        )

        self.assertEqual(len(responses), 1)
        resp = responses[0]
        expected_ts = '2021-12-20 12:18:40+01:00'
        expected_record = f"(140, 99, 12, 20.5, '{expected_ts}')," \
                          f"(140, 99, 14, 37.43, '{expected_ts}')," \
                          f"(140, 99, 15, 55, '{expected_ts}')," \
                          f"(140, 99, 16, 60, '{expected_ts}')"
        self.assertEqual(resp.measure_record, expected_record)

    @property
    def get_test_add_places_requests(self):
        geolocation = PostgisPoint(latitude=45, longitude=9, srid=4326)
        return AddPlacesRequest(
            placename="Pavia",
            poscode="27100",
            state="Lombardia",
            geolocation=geolocation,
            countrycode="IT",
            province="Pavia"
        )

    ##################################### test_create_response_to_request_of_adding_places #####################################
    def test_create_response_to_request_of_adding_places(self):
        mocked_valid_requests = MagicMock()
        mocked_valid_requests.__len__.return_value = 1
        mocked_valid_requests.__iter__.return_value = [self.get_test_add_places_requests]

        responses = AddPlacesResponseBuilder(requests=mocked_valid_requests, service_id=1)
        self.assertEqual(len(responses), 1)

        resp = responses[0]
        expected_place_record = "(1, '27100', 'IT', 'Pavia', 'Pavia', 'Lombardia', ST_GeomFromText('POINT(9 45)', 4326))"
        self.assertEqual(resp.place_record, expected_place_record)

    @property
    def get_test_current_weather_request(self):
        return AddWeatherForecastRequest(
            timestamp=datetime.utcfromtimestamp(1641217631+3600),
            temperature=8.84,
            pressure=1018,
            humidity=81,
            wind_speed=0.59,
            wind_direction=106,
            weather_id=55
        )

    @property
    def get_test_hourly_forecast_request(self):
        return AddWeatherForecastRequest(
            timestamp=datetime.utcfromtimestamp(1641214800+3600),
            temperature=9.21,
            pressure=1018,
            humidity=80,
            wind_speed=0.33,
            wind_direction=186,
            rain=0.21,
            weather_id=55
        )

    @property
    def get_test_daily_forecast_request(self):
        return AddWeatherForecastRequest(
            timestamp=datetime.utcfromtimestamp(1641207600+3600),
            temperature=9.25,
            min_temp=5.81,
            max_temp=9.4,
            pressure=1019,
            humidity=83,
            wind_speed=2.72,
            wind_direction=79,
            weather_id=55
        )

    @property
    def get_test_add_openweathermap_data_request(self):
        return AddOpenWeatherMapDataRequest(
            current=self.get_test_current_weather_request,
            hourly=[self.get_test_hourly_forecast_request],
            daily=[self.get_test_daily_forecast_request]
        )

    ##################################### test_create_response_to_request_of_adding_openweathermap_data #####################################
    def test_create_response_to_request_of_adding_openweathermap_data(self):

        mocked_request_builder = MagicMock()
        mocked_request_builder.__len__.return_value = 1
        mocked_request_builder.__iter__.return_value = [self.get_test_add_openweathermap_data_request]

        response_builder = AddOpenWeatherMapDataResponseBuilder(
            requests=mocked_request_builder, service_id=1, geoarea_id=14400
        )
        self.assertEqual(len(response_builder), 1)

        resp = response_builder[0]
        expected_current_record = "(1, 14400, 55, 8.84, 1018, 81, 0.59, 106, NULL, NULL, '2022-01-03 14:47:11')"
        self.assertEqual(resp.current_weather_record, expected_current_record)

        expected_hourly_record = "(1, 14400, 55, 9.21, 1018, 80, 0.33, 186, 0.21, NULL, '2022-01-03 14:00:00')"
        self.assertEqual(resp.hourly_forecast_record, expected_hourly_record)

        expected_daily_record = "(1, 14400, 55, 9.25, 5.81, 9.4, 1019, 83, 2.72, 79, NULL, NULL, '2022-01-03 12:00:00')"
        self.assertEqual(resp.daily_forecast_record, expected_daily_record)


if __name__ == '__main__':
    main()
