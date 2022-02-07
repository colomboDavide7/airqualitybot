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
import airquality.usecase as constants
from airquality.usecase.abc import UsecaseABC
from airquality.datamodel.fromfile import CityDM
from airquality.extra.decorator import log_context
from airquality.extra.sqlize import sqlize_iterable
from airquality.extra.url import json_http_response
from airquality.database.gateway import DatabaseGateway
from airquality.iterables.requests import OpenweathermapIterableRequests
from airquality.iterables.validator import WeatherDataIterableValidRequests
from airquality.iterables.responses import WeatherDataIterableResponses
from airquality.iterables.fromapi import OpenweathermapIterableDatamodels
from airquality.iterables.fromfile import CityIterableDatamodels


class Openweathermap(UsecaseABC):

    DELETE_FORECAST_QUERY = "DELETE FROM level0_raw.hourly_forecast; DELETE FROM level0_raw.daily_forecast;"
    HOURLY_FORECAST_QUERY = "INSERT INTO level0_raw.hourly_forecast (id, geoarea_id, weather_id, temperature, pressure,"\
                            " humidity, wind_speed, wind_direction, rain, pop, snow, timestamp) VALUES {val};"
    DAILY_FORECAST_QUERY = "INSERT INTO level0_raw.daily_forecast (id, geoarea_id, weather_id, temperature, min_temp, "\
                           "max_temp, pressure, humidity, wind_speed, wind_direction, rain, pop, snow, timestamp) " \
                           "VALUES {val};"

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
            valid_requests = WeatherDataIterableValidRequests(
                requests=requests,
                fexists=self._database_gway.exists_weather_alert_of,
                extra={'geoarea_id': geoarea_info.id}
            )
            responses = WeatherDataIterableResponses(requests=valid_requests, geoarea_id=geoarea_info.id)
            self._database_gway.execute(query=responses.query())
            _LOGGER.debug("inserted weather data for city = '%s'" % str(city))

            self._cached_hourly_forecast = [item for item in self._cached_hourly_forecast if item[1] != geoarea_info.id]
            self._cached_daily_forecast = [item for item in self._cached_daily_forecast if item[1] != geoarea_info.id]

        except ValueError as err:
            _LOGGER.warning("%s" % str(err))

# =========== EXECUTE METHOD
    @log_context(logger_name=__name__, header=constants.START_MESSAGE, teardown=constants.END_MESSAGE)
    def execute(self):
        try:
            for city in self._cities:
                self._safe_insert_weather_data_of(city=city)
        except BaseException:
            if self._cached_hourly_forecast and self._cached_daily_forecast:
                query = self.HOURLY_FORECAST_QUERY.format(
                    val=','.join(sqlize_iterable(item) for item in self._cached_hourly_forecast)
                )
                query += self.DAILY_FORECAST_QUERY.format(
                    val=','.join(sqlize_iterable(item) for item in self._cached_daily_forecast)
                )
                self._database_gway.execute(query=query)
            raise
