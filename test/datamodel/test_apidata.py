######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 15:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.datamodel.apidata import PurpleairAPIData, AtmotubeAPIData, ThingspeakAPIData, GeonamesData, \
    Weather, WeatherForecast, OpenWeatherMapAPIData


class TestDatamodel(TestCase):

    def test_purpleair_apidata_model(self):
        data = PurpleairAPIData(
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

        self.assertEqual(data.name, "fakename")
        self.assertEqual(data.sensor_index, 9)
        self.assertEqual(data.latitude, 1.234)
        self.assertEqual(data.longitude, 5.666)
        self.assertEqual(data.altitude, 0)
        self.assertEqual(data.primary_id_a, 111)
        self.assertEqual(data.primary_key_a, "key1a")
        self.assertEqual(data.primary_id_b, 222)
        self.assertEqual(data.primary_key_b, "key1b")
        self.assertEqual(data.secondary_id_a, 333)
        self.assertEqual(data.secondary_key_a, "key2a")
        self.assertEqual(data.secondary_id_b, 444)
        self.assertEqual(data.secondary_key_b, "key2b")

    def test_atmotube_apidata_model(self):
        data = AtmotubeAPIData(
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

        self.assertEqual(data.time, "2021-08-10T23:59:00.000Z")
        self.assertEqual(data.voc, 0.17)
        self.assertEqual(data.pm1, 8)
        self.assertEqual(data.pm25, 10)
        self.assertEqual(data.pm10, 11)
        self.assertEqual(data.t, 29)
        self.assertEqual(data.h, 42)
        self.assertEqual(data.p, 1004.68)
        self.assertEqual(data.coords, {'lat': 45.765, 'lon': 9.897})

    def test_thingspeak_primary_channel_a_apidata_model(self):
        data = ThingspeakAPIData(
            created_at="2021-12-20T11:18:40Z",
            field1="20.50",
            field2="35.53",
            field3="37.43",
            field6="55",
            field7="60"
        )

        self.assertEqual(data.created_at, "2021-12-20T11:18:40Z")
        self.assertEqual(data.field1, 20.50)
        self.assertEqual(data.field2, 35.53)
        self.assertEqual(data.field3, 37.43)
        self.assertEqual(data.field6, 55)
        self.assertEqual(data.field7, 60)
        self.assertIsNone(data.field4)
        self.assertIsNone(data.field5)

    def test_thingspeak_primary_channel_b_apidata_model(self):
        data = ThingspeakAPIData(
            created_at="2021-12-19T11:06:25Z",
            field1="126.65",
            field2="222.24",
            field3="283.44",
            field6="1016.49",
        )
        self.assertEqual(data.created_at, "2021-12-19T11:06:25Z")
        self.assertEqual(data.field1, 126.65)
        self.assertEqual(data.field2, 222.24)
        self.assertEqual(data.field3, 283.44)
        self.assertEqual(data.field6, 1016.49)
        self.assertIsNone(data.field7)
        self.assertIsNone(data.field4)
        self.assertIsNone(data.field5)

    def test_thingspeak_secondary_channel_a_apidata_model(self):
        data = ThingspeakAPIData(
            created_at="2021-12-19T11:06:23Z",
            field1="10544.95",
            field2="2980.84",
            field3="724.11",
            field4="127.53",
            field5="28.51",
            field6="2.25",
        )
        self.assertEqual(data.created_at, "2021-12-19T11:06:23Z")
        self.assertEqual(data.field1, 10544.95)
        self.assertEqual(data.field2, 2980.84)
        self.assertEqual(data.field3, 724.11)
        self.assertEqual(data.field4, 127.53)
        self.assertEqual(data.field5, 28.51)
        self.assertEqual(data.field6, 2.25)
        self.assertIsNone(data.field7)

    def test_thingspeak_secondary_channel_b_apidata_model(self):
        data = ThingspeakAPIData(
            created_at="2021-12-09T15:54:34Z",
            field1="10544.95",
            field2="2980.84",
            field3="724.11",
            field4="127.53",
            field5="28.51",
            field6="2.25",
        )
        self.assertEqual(data.created_at, "2021-12-09T15:54:34Z")
        self.assertEqual(data.field1, 10544.95)
        self.assertEqual(data.field2, 2980.84)
        self.assertEqual(data.field3, 724.11)
        self.assertEqual(data.field4, 127.53)
        self.assertEqual(data.field5, 28.51)
        self.assertEqual(data.field6, 2.25)
        self.assertIsNone(data.field7)

    def test_geonames_country_data(self):
        line = ["IT", "27100", "Pavia'", "Lombardia'", "statecode", "Pavia'", "PV", "community", "communitycode", "45", "9", "4"]
        data = GeonamesData(*line)

        self.assertEqual(data.postal_code, "27100")
        self.assertEqual(data.place_name, "Pavia")
        self.assertEqual(data.country_code, "IT")
        self.assertEqual(data.state, "Lombardia")
        self.assertEqual(data.province, "Pavia")
        self.assertEqual(data.latitude, 45)
        self.assertEqual(data.longitude, 9)

    ########################################## test_onecall_apidata ##########################################
    def test_onecall_apidata(self):
        test_current_weather_data = Weather(
            main="Clouds",
            description="overcast clouds"
        )

        test_current = WeatherForecast(
            dt=1641217631,
            temp=8.84,
            pressure=1018,
            humidity=81,
            wind_speed=0.59,
            wind_deg=106,
            weather=[test_current_weather_data]
        )

        test_hourly_forecast_weather = Weather(
            main="Clouds",
            description="overcast clouds"
        )

        test_hourly_forecast = WeatherForecast(
            dt=1641214800,
            temp=9.21,
            pressure=1018,
            humidity=80,
            wind_speed=0.33,
            wind_deg=186,
            weather=[test_hourly_forecast_weather]
        )

        test_daily_forecast_weather = Weather(
            main="Clouds",
            description="overcast clouds"
        )

        test_daily_forecast = WeatherForecast(
            dt=1641207600,
            temp=9.25,
            temp_min=5.81,
            temp_max=9.4,
            pressure=1019,
            humidity=83,
            wind_speed=2.72,
            wind_deg=79,
            weather=[test_daily_forecast_weather]
        )

        data = OpenWeatherMapAPIData(
            current=test_current,
            hourly_forecast=[test_hourly_forecast],
            daily_forecast=[test_daily_forecast]
        )

        self.assertEqual(data.current, test_current)
        self.assertEqual(data.hourly_forecast[0], test_hourly_forecast)
        self.assertEqual(data.daily_forecast[0], test_daily_forecast)


if __name__ == '__main__':
    main()
