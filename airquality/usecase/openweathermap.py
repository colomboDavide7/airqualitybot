######################################################
#
# Author: Davide Colombo
# Date: 03/01/22 20:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
import airquality.environment as environ

_LOGGER = logging.getLogger(__name__)
_ENVIRON = environ.get_environ()

######################################################
import os
from typing import Set
import airquality.usecase as constants
from airquality.usecase.abc import UsecaseABC
from airquality.datamodel.fromfile import CityDM
from airquality.extra.decorator import log_context
from airquality.extra.sqlize import sqlize_iterable
from airquality.extra.url import json_http_response
from airquality.database.gateway import DatabaseGateway
from airquality.iterables.requests import OpenweathermapIterableRequests
from airquality.iterables.responses import WeatherDataIterableResponses
from airquality.iterables.fromapi import OpenweathermapIterableDatamodels
from airquality.iterables.fromfile import CityIterableDatamodels


# def _build_insert_query(response_builder: WeatherDataIterableResponses):
#     cval = hval = dval = aval = ""
#     for resp in response_builder:
#         cval += f"{resp.current_weather_record},"
#         hval += f"{resp.hourly_forecast_record},"
#         dval += f"{resp.daily_forecast_record},"
#         aval += f"{resp.weather_alert_record},"
#     query = "INSERT INTO level0_raw.current_weather " \
#             "(geoarea_id, weather_id, temperature, pressure, humidity, wind_speed, " \
#             "wind_direction, rain, snow, timestamp, sunrise, sunset) " \
#             f"VALUES {cval.strip(',')};"
#     query += "INSERT INTO level0_raw.hourly_forecast " \
#              "(geoarea_id, weather_id, temperature, pressure, humidity, " \
#              "wind_speed, wind_direction, rain, pop, snow, timestamp) " \
#              f"VALUES {hval.strip(',')};"
#     query += "INSERT INTO level0_raw.daily_forecast " \
#              "(geoarea_id, weather_id, temperature, min_temp, max_temp, pressure, " \
#              "humidity, wind_speed, wind_direction, rain, pop, snow, timestamp) " \
#              f"VALUES {dval.strip(',')};"
#     query += "" if not aval.strip(',') else \
#              "INSERT INTO level0_raw.weather_alert " \
#              "(geoarea_id, sender_name, alert_event, " \
#              "alert_begin, alert_until, description) " \
#              f"VALUES {aval.strip(',')};"
#     return query


def _build_insert_cached_forecast_records_query(hourly: Set, daily: Set) -> str:
    return "INSERT INTO level0_raw.hourly_forecast " \
           "(id, geoarea_id, weather_id, temperature, pressure, humidity, " \
           "wind_speed, wind_direction, rain, pop, snow, timestamp) " \
           f"VALUES {','.join(sqlize_iterable(item) for item in hourly)};" \
           "INSERT INTO level0_raw.daily_forecast" \
           "(id, geoarea_id, weather_id, temperature, min_temp, max_temp, pressure, " \
           "humidity, wind_speed, wind_direction, rain, pop, snow, timestamp) " \
           f"VALUES {','.join(sqlize_iterable(item) for item in daily)};"


class AddWeatherData(UsecaseABC):

    DELETE_FORECAST_QUERY = "DELETE FROM level0_raw.hourly_forecast; DELETE FROM level0_raw.daily_forecast;"

    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        # Database resources
        self._api_keys = self._database_gway.query_openweathermap_keys()
        self._weather_map = self._database_gway.query_weather_conditions()
        self._cached_hourly_forecast = self._database_gway.query_hourly_forecast_records()
        self._cached_daily_forecast = self._database_gway.query_daily_forecast_records()
        self._database_gway.execute(query=self.DELETE_FORECAST_QUERY)
        # File System resources
        self._dir_path = _ENVIRON.input_dir_of(personality='openweathermap')
        self._url_template = _ENVIRON.url_template(personality='openweathermap')
        self._cities = CityIterableDatamodels(filepath=os.path.join(self._dir_path, 'cities.json'))

# =========== SAFE METHOD
    def _safe_insert_weather_data_of(self, city: CityDM):
        try:
            geoarea_info = self._database_gway.query_place_location(
                country_code=city.country_code,
                place_name=city.place_name
            )
            key_to_use = self._api_keys[0].key      # using only the first key for now
            url = self._url_template.format(
                api_key=key_to_use,
                lat=geoarea_info.latitude,
                lon=geoarea_info.longitude
            )
            service_jresp = json_http_response(url=url)
            datamodels = OpenweathermapIterableDatamodels(json_response=service_jresp)
            requests = OpenweathermapIterableRequests(datamodels=datamodels, weather_map=self._weather_map)
            responses = WeatherDataIterableResponses(requests=requests, geoarea_id=geoarea_info.id)
            self._database_gway.execute(query=responses.query())
            _LOGGER.debug("inserted weather data for city = '%s'" % str(city))
        except ValueError as err:
            _LOGGER.warning("%s" % str(err))

# =========== EXECUTE METHOD
    @log_context(logger_name=__name__, header=constants.START_MESSAGE, teardown=constants.END_MESSAGE)
    def execute(self):
        try:
            for city in self._cities:
                self._safe_insert_weather_data_of(city=city)
        except Exception as err:
            if not isinstance(err, SystemExit) and not isinstance(err, KeyboardInterrupt):
                if self._cached_hourly_forecast and self._cached_daily_forecast:
                    self._database_gway.execute(
                        query=_build_insert_cached_forecast_records_query(
                            hourly=self._cached_hourly_forecast,
                            daily=self._cached_daily_forecast)
                    )
            raise
