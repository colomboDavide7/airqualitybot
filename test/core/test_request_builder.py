######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:00
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.request import Channel
from airquality.datamodel.geometry import NullGeometry, PostgisPoint
from airquality.datamodel.apidata import PurpleairAPIData, AtmotubeAPIData, ThingspeakAPIData, GeonamesData, \
    Weather, WeatherForecast, OpenWeatherMapAPIData
from airquality.core.request_builder import AddPurpleairSensorRequestBuilder, AddAtmotubeMeasureRequestBuilder, \
    AddThingspeakMeasuresRequestBuilder, AddPlacesRequestBuilder, AddOpenWeatherMapDataRequestBuilder


class TestRequestBuilder(TestCase):

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

    ##################################### test_create_request_for_adding_purpleair_sensor #####################################
    def test_create_request_for_adding_purpleair_sensor(self):
        mocked_datamodel_builder = MagicMock()
        mocked_datamodel_builder.__iter__.return_value = [self.get_test_purpleair_datamodel]

        requests = AddPurpleairSensorRequestBuilder(datamodel=mocked_datamodel_builder)
        self.assertEqual(len(requests), 1)
        req1 = requests[0]

        expected_last_acquisition = datetime.fromtimestamp(1234567890)
        expected_api_param = [
            Channel(api_key="key1a", api_id="111", channel_name="1A", last_acquisition=expected_last_acquisition),
            Channel(api_key="key1b", api_id="222", channel_name="1B", last_acquisition=expected_last_acquisition),
            Channel(api_key="key2a", api_id="333", channel_name="2A", last_acquisition=expected_last_acquisition),
            Channel(api_key="key2b", api_id="444", channel_name="2B", last_acquisition=expected_last_acquisition)
        ]
        expected_geolocation = PostgisPoint(latitude=1.234, longitude=5.666)

        self.assertEqual(req1.type, "Purpleair/Thingspeak")
        self.assertEqual(req1.name, "fakename (9)")
        self.assertEqual(req1.channels, expected_api_param)
        self.assertEqual(req1.geolocation, expected_geolocation)

    @property
    def get_test_atmotube_datamodel(self):
        return AtmotubeAPIData(
            time="2021-08-10T23:59:00.000Z",
            voc=0.17,
            pm1=8,
            pm25=10,
            pm10=11,
            t=29,
            h=42,
            p=1004.68,
            coords={'lat': 45.765, 'lon': 9.897}
        )

    @property
    def get_test_atmotube_datamodel_without_coords(self):
        return AtmotubeAPIData(
            time="2021-08-11T00:00:00.000Z",
            voc=0.19,
            pm1=7,
            p=1007.03
        )

    ##################################### test_create_request_for_adding_atmotube_measure #####################################
    def test_create_request_for_adding_atmotube_measure(self):
        test_code2id = {'voc': 66, 'pm1': 48, 'pm25': 94, 'pm10': 2, 't': 4, 'h': 12, 'p': 39}
        mocked_datamodel_builder = MagicMock()
        mocked_datamodel_builder.__iter__.return_value = [self.get_test_atmotube_datamodel, self.get_test_atmotube_datamodel_without_coords]

        requests = AddAtmotubeMeasureRequestBuilder(datamodel=mocked_datamodel_builder, code2id=test_code2id)
        self.assertEqual(len(requests), 2)
        req1 = requests[0]

        expected_timestamp = datetime.strptime("2021-08-10T23:59:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        expected_geolocation = PostgisPoint(latitude=45.765, longitude=9.897)
        expected_measures = [(66, 0.17), (48, 8), (94, 10), (2, 11), (4, 29), (12, 42), (39, 1004.68)]

        self.assertEqual(req1.timestamp, expected_timestamp)
        self.assertEqual(req1.geolocation, expected_geolocation)
        self.assertEqual(req1.measures, expected_measures)

        req2 = requests[1]
        expected_timestamp = datetime.strptime("2021-08-11T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        expected_measures = [(66, 0.19), (48, 7), (39, 1007.03)]
        self.assertEqual(req2.timestamp, expected_timestamp)
        self.assertEqual(req2.measures, expected_measures)
        self.assertIsInstance(req2.geolocation, NullGeometry)

    @property
    def get_test_thingspeak_primary_channel_a_datamodel(self):
        return ThingspeakAPIData(
            created_at="2021-12-20T11:18:40Z",
            field1="20.50",
            field2=None,
            field3="37.43",
            field6="55",
            field7="60"
        )

    ############################## test_create_request_for_adding_thingspeak_primary_channel_a_data #############################
    def test_create_request_for_adding_thingspeak_primary_channel_a_measures(self):

        test_field_map = {'field1': 'p1', 'field2': 'p2', 'field3': 'p3', 'field6': 'p6', 'field7': 'p7'}
        test_code2id = {'p1': 12, 'p2': 13, 'p3': 14, 'p6': 15, 'p7': 16}
        mocked_datamodel_builder = MagicMock()
        mocked_datamodel_builder.__iter__.return_value = [self.get_test_thingspeak_primary_channel_a_datamodel]

        requests = AddThingspeakMeasuresRequestBuilder(
            datamodel=mocked_datamodel_builder, code2id=test_code2id, field_map=test_field_map
        )
        self.assertEqual(len(requests), 1)
        req = requests[0]

        expected_timestamp = datetime.strptime("2021-12-20T11:18:40Z", "%Y-%m-%dT%H:%M:%SZ")
        expected_measures = [(12, 20.50), (14, 37.43), (15, 55), (16, 60)]
        self.assertEqual(req.timestamp, expected_timestamp)
        self.assertEqual(req.measures, expected_measures)

    ############################## test_create_request_for_adding_thingspeak_primary_channel_b_data #############################
    def test_create_request_for_adding_thingspeak_primary_channel_b_measures(self):
        test_field_map = {'field1': 'p1', 'field2': 'p2', 'field3': 'p3', 'field6': 'p6'}
        test_code2id = {'p1': 12, 'p2': 13, 'p3': 14, 'p6': 15, 'p7': 16}
        mocked_datamodel_builder = MagicMock()
        mocked_datamodel_builder.__iter__.return_value = [self.get_test_thingspeak_primary_channel_a_datamodel]

        requests = AddThingspeakMeasuresRequestBuilder(
            datamodel=mocked_datamodel_builder, code2id=test_code2id, field_map=test_field_map
        )
        self.assertEqual(len(requests), 1)
        req = requests[0]

        expected_timestamp = datetime.strptime("2021-12-20T11:18:40Z", "%Y-%m-%dT%H:%M:%SZ")
        expected_measures = [(12, 20.50), (14, 37.43), (15, 55.0)]
        self.assertEqual(req.timestamp, expected_timestamp)
        self.assertEqual(req.measures, expected_measures)

    @property
    def get_test_geonames_data(self):
        line = ["IT", "27100", "Pavia'", "Lombardia'", "statecode", "Pavia'", "PV", "community", "communitycode", "45", "9", "4"]
        return GeonamesData(*line)

    ############################## test_create_requests_for_adding_places #############################
    def test_create_requests_for_adding_places(self):
        mocked_datamodel_builder = MagicMock()
        mocked_datamodel_builder.__len__.return_value = 1
        mocked_datamodel_builder.__iter__.return_value = [self.get_test_geonames_data]

        requests = AddPlacesRequestBuilder(datamodels=mocked_datamodel_builder)
        self.assertEqual(len(requests), 1)
        req = requests[0]

        expected_geolocation = PostgisPoint(latitude=45, longitude=9, srid=4326)
        self.assertEqual(req.poscode, "27100")
        self.assertEqual(req.geolocation, expected_geolocation)
        self.assertEqual(req.placename, "Pavia")
        self.assertEqual(req.state, "Lombardia")
        self.assertEqual(req.province, "Pavia")
        self.assertEqual(req.countrycode, "IT")

    @property
    def get_test_current_weather_data(self):
        return WeatherForecast(
            dt=1641217631+3600,
            temp=8.84,
            pressure=1018,
            humidity=81,
            wind_speed=0.59,
            wind_deg=106,
            weather=[Weather(main="Clouds", description="overcast clouds")]
        )

    @property
    def get_test_hourly_forecast_data(self):
        return WeatherForecast(
            dt=1641214800+3600,
            temp=9.21,
            pressure=1018,
            humidity=80,
            wind_speed=0.33,
            wind_deg=186,
            weather=[Weather(main="Clouds", description="overcast clouds")],
            rain=0.21
        )

    @property
    def get_test_daily_forecast_data(self):
        return WeatherForecast(
            dt=1641207600+3600,
            temp=9.25,
            temp_min=5.81,
            temp_max=9.4,
            pressure=1019,
            humidity=83,
            wind_speed=2.72,
            wind_deg=79,
            weather=[Weather(main="Clouds", description="overcast clouds")]
        )

    @property
    def get_test_openweathermap_apidata(self):
        return OpenWeatherMapAPIData(
            current=self.get_test_current_weather_data,
            hourly_forecast=[self.get_test_hourly_forecast_data],
            daily_forecast=[self.get_test_daily_forecast_data]
        )

    ############################## test_create_request_for_adding_openweathermap_data #############################
    def test_create_request_for_adding_openweathermap_data(self):
        mocked_datamodel_builder = MagicMock()
        mocked_datamodel_builder.__len__.return_value = 1
        mocked_datamodel_builder.__iter__.return_value = [self.get_test_openweathermap_apidata]

        test_code2id = {
            'temp': 1, 'temp_min': 2, 'temp_max': 3, 'pressure': 4, 'humidity': 5, 'wind_speed': 6,
            'wind_deg': 7, 'rain': 8, 'snow': 9
        }

        requests = AddOpenWeatherMapDataRequestBuilder(
            datamodels=mocked_datamodel_builder, code2id=test_code2id
        )
        self.assertEqual(len(requests), 1)

        req = requests[0]
        self.assertEqual(req.current.timestamp, datetime.utcfromtimestamp(1641217631+3600))
        self.assertEqual(req.current.weather, "Clouds")
        self.assertEqual(req.current.description, "overcast clouds")
        expected_current_measures = [(1, 8.84), (4, 1018), (5, 81), (6, 0.59), (7, 106)]
        self.assertEqual(req.current.measures, expected_current_measures)

        hourly1 = req.hourly[0]
        self.assertEqual(hourly1.timestamp, datetime.utcfromtimestamp(1641214800+3600))
        self.assertEqual(hourly1.weather, "Clouds")
        self.assertEqual(hourly1.description, "overcast clouds")

        expected_hourly_measures = [(1, 9.21), (4, 1018), (5, 80), (6, 0.33), (7, 186), (8, 0.21)]
        self.assertEqual(hourly1.measures, expected_hourly_measures)

        daily1 = req.daily[0]
        self.assertEqual(daily1.timestamp, datetime.utcfromtimestamp(1641207600+3600))
        self.assertEqual(daily1.weather, "Clouds")
        self.assertEqual(daily1.description, "overcast clouds")
        expected_daily_measures = [(1, 9.25), (2, 5.81), (3, 9.4), (4, 1019), (5, 83), (6, 2.72), (7, 79)]
        self.assertEqual(daily1.measures, expected_daily_measures)


if __name__ == '__main__':
    main()
