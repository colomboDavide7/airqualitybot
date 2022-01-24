######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.datamodel.response import AddFixedSensorResponse, \
                                          AddMobileMeasureResponse, \
                                          AddStationMeasuresResponse, \
                                          AddPlacesResponse, \
                                          AddOpenWeatherMapDataResponse


class TestResponseModel(TestCase):

    def test_add_fixed_sensors_response(self):
        response = AddFixedSensorResponse(
            sensor_record="fake_sensor_record",
            apiparam_record="fake_apiparam_record",
            geolocation_record="fake_geo_record"
        )
        self.assertEqual(response.sensor_record, "fake_sensor_record")
        self.assertEqual(response.apiparam_record, "fake_apiparam_record")
        self.assertEqual(response.geolocation_record, "fake_geo_record")

    def test_add_mobile_measures_response(self):
        response = AddMobileMeasureResponse(
            measure_record="fake_measure_record"
        )
        self.assertEqual(response.measure_record, "fake_measure_record")

    def test_add_station_measures_response(self):
        response = AddStationMeasuresResponse(
            measure_record="fake_measure_records"
        )
        self.assertEqual(response.measure_record, "fake_measure_records")

    def test_add_places_response(self):
        response = AddPlacesResponse(
            place_record="fake_place_record"
        )
        self.assertEqual(response.place_record, "fake_place_record")

    def test_add_openweathermap_data_response(self):
        response = AddOpenWeatherMapDataResponse(
            current_weather_record="fake_current",
            hourly_forecast_record="fake_hourly",
            daily_forecast_record="fake_daily",
            weather_alert_record='fake_alert'
        )
        self.assertEqual(response.current_weather_record, "fake_current")
        self.assertEqual(response.hourly_forecast_record, "fake_hourly")
        self.assertEqual(response.daily_forecast_record, "fake_daily")
        self.assertEqual(response.weather_alert_record, 'fake_alert')


if __name__ == '__main__':
    main()
