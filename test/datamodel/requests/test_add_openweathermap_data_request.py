######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from airquality.datamodel.request import AddWeatherForecastRequest, AddOpenWeatherMapDataRequest


class TestAddOpenweathermapDataRequest(TestCase):

# =========== TEST METHODS
    def test_add_openweathermap_data_request(self):

        current_weather_request = AddWeatherForecastRequest(
            timestamp=datetime.fromtimestamp(1641217631+3600),
            temperature=8.84,
            pressure=1018,
            humidity=81,
            wind_speed=0.59,
            wind_direction=106,
            weather_id=55
        )

        hourly_forecast_request = AddWeatherForecastRequest(
            timestamp=datetime.fromtimestamp(1641214800+3600),
            temperature=9.21,
            pressure=1018,
            humidity=80,
            wind_speed=0.33,
            wind_direction=186,
            rain=0.21,
            weather_id=55
        )

        daily_forecast_request = AddWeatherForecastRequest(
            timestamp=datetime.fromtimestamp(1641207600+3600),
            temperature=9.25,
            min_temp=5.81,
            max_temp=9.4,
            pressure=1019,
            humidity=83,
            wind_speed=2.72,
            wind_direction=79,
            weather_id=55
        )

        request = AddOpenWeatherMapDataRequest(
            current=current_weather_request,
            hourly=[hourly_forecast_request],
            daily=[daily_forecast_request]
        )

        self.assertEqual(request.current, current_weather_request)
        self.assertEqual(request.hourly[0], hourly_forecast_request)
        self.assertEqual(request.daily[0], daily_forecast_request)


if __name__ == '__main__':
    main()
