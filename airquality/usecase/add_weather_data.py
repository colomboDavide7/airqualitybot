######################################################
#
# Author: Davide Colombo
# Date: 03/01/22 20:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
import airquality.environment as environ
from airquality.extra.timest import openweathermap_timest

_LOGGER = logging.getLogger(__name__)
_ENVIRON = environ.get_environ()
_TIMEST = openweathermap_timest()

######################################################
from typing import Dict, Set
import airquality.usecase as constants
from airquality.extra.sqlize import sqlize
from airquality.usecase.abc import UsecaseABC
from airquality.url.url_reader import json_http_response
from airquality.datamodel.apidata import WeatherCityData
from airquality.database.gateway import DatabaseGateway
from airquality.core.request_builder import AddOpenWeatherMapDataRequestBuilder
from airquality.core.response_builder import AddOpenWeatherMapDataResponseBuilder
from airquality.core.apidata_builder import OpenWeatherMapAPIDataBuilder, WeatherCityDataBuilder

_DELETE_FORECAST_QUERY = "DELETE FROM level0_raw.hourly_forecast; DELETE FROM level0_raw.daily_forecast;"


# def _build_insert_query(response_builder: AddOpenWeatherMapDataResponseBuilder):
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


def _build_insert_query(response_builder: AddOpenWeatherMapDataResponseBuilder):
    cval = hval = dval = aval = ""
    for resp in response_builder:
        cval += f"{resp.current_weather_record},"
        hval += f"{resp.hourly_forecast_record},"
        dval += f"{resp.daily_forecast_record},"
        aval += f"{resp.weather_alert_record},"
    query = "INSERT INTO level0_raw.current_weather " \
            "(geoarea_id, weather_id, temperature, pressure, humidity, wind_speed, " \
            "wind_direction, rain, snow, timestamp, sunrise, sunset) " \
            f"VALUES {cval.strip(',')};"
    query += "INSERT INTO level0_raw.hourly_forecast " \
             "(geoarea_id, weather_id, temperature, pressure, humidity, " \
             "wind_speed, wind_direction, rain, pop, snow, timestamp) " \
             f"VALUES {hval.strip(',')};"
    query += "INSERT INTO level0_raw.daily_forecast " \
             "(geoarea_id, weather_id, temperature, min_temp, max_temp, pressure, " \
             "humidity, wind_speed, wind_direction, rain, pop, snow, timestamp) " \
             f"VALUES {dval.strip(',')};"
    query += "" if not aval.strip(',') else \
             "INSERT INTO level0_raw.weather_alert " \
             "(geoarea_id, sender_name, alert_event, " \
             "alert_begin, alert_until, description) " \
             f"VALUES {aval.strip(',')};"
    return query


def _build_insert_cached_forecast_records_query(hourly: Set, daily: Set) -> str:
    return "INSERT INTO level0_raw.hourly_forecast " \
           "(id, geoarea_id, weather_id, temperature, pressure, humidity, " \
           "wind_speed, wind_direction, rain, pop, snow, timestamp) " \
           f"VALUES {','.join(sqlize(item) for item in hourly)};" \
           "INSERT INTO level0_raw.daily_forecast" \
           "(id, geoarea_id, weather_id, temperature, min_temp, max_temp, pressure, " \
           "humidity, wind_speed, wind_direction, rain, pop, snow, timestamp) " \
           f"VALUES {','.join(sqlize(item) for item in daily)};"


class AddWeatherData(UsecaseABC):
    """
    An *object* that defines the application UseCase flow of adding weather data from OpenWeatherMap service.

    The data are downloaded from the site by using the OneCallAPI service whose documentation is linked at:
    https://openweathermap.org/api/one-call-api#data

    The data are uploaded by-city. The cities one is interested of must be inserted into the
    *weather_cities.json* file provided into the resources directory of this project.

    The task accomplished by this class is to retrieve the data for each city present into the file cited above
    using the API cited above.

    The data are of three types:

    - current weather data,
    - hourly forecast data for the next 48 hours,
    - daily forecast data for the next 7 days.

    If the API has provided some data, those are inserted into the database.
    """

    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._cached_weather_map = self._weather_map()
        self._cached_url_template = _ENVIRON.url_template(personality='openweathermap')
        self._cached_cities = WeatherCityDataBuilder(filepath='resources/weather_cities.json')
        self._api_keys = self._database_gway.query_openweathermap_keys()
        self._cached_hourly_forecast = self._database_gway.query_hourly_forecast_records()
        self._cached_daily_forecast = self._database_gway.query_daily_forecast_records()

    def _weather_map(self) -> Dict[int, Dict[str, int]]:
        rows = self._database_gway.query_weather_conditions()
        weather_map = {code: {} for id_, code, icon in rows}
        for id_, code, icon in rows:
            weather_map[code][icon] = id_
        return weather_map

    def _delete_forecast_measures(self):
        _LOGGER.warning("deleting all the HOURLY and DAILY weather forecast data")
        self._database_gway.execute(query=_DELETE_FORECAST_QUERY)

# =========== SAFE METHOD
    def _safe_insert_weather_of(self, api_key: str, city: WeatherCityData):
        """
        This method handles the possibility that a *ValueError* exception is raised by the *database_gateway* when
        try to query the geolocation of the current *city*.

        In that case the application won't stop, but it takes the next city in the file.

        The exception is safely logged for debug purposes.

        :param api_key:                 the service's API key to use for downloading the data.
        :param city:                    the weather city data object that refers to the current city.
        """

        try:
            geoarea_info = self._database_gway.query_geolocation_of(
                country_code=city.country_code,
                place_name=city.place_name
            )
            _LOGGER.debug("found database correspondence for => %s" % repr(geoarea_info))
        except ValueError:
            _LOGGER.warning("Cannot found database correspondence for => %s" % repr(city))
            return

        pre_formatted_url = self._cached_url_template.format(
            api_key=api_key,
            lat=geoarea_info.latitude,
            lon=geoarea_info.longitude
        )
        _LOGGER.debug(f"downloading weather data at => {pre_formatted_url}")

        service_jresp = json_http_response(url=pre_formatted_url)
        _LOGGER.debug("successfully get server response!!!")

        datamodel_builder = OpenWeatherMapAPIDataBuilder(json_response=service_jresp)
        _LOGGER.debug("found #%d API data" % len(datamodel_builder))

        request_builder = AddOpenWeatherMapDataRequestBuilder(
            datamodels=datamodel_builder,
            weather_map=self._cached_weather_map,
            timest=_TIMEST
        )
        _LOGGER.debug("found #%d requests" % len(request_builder))

        response_builder = AddOpenWeatherMapDataResponseBuilder(
            requests=request_builder,
            geoarea_id=geoarea_info.geoarea_id
        )
        _LOGGER.debug("found #%d responses" % len(response_builder))

        if len(response_builder) > 0:
            _LOGGER.debug("inserting new weather data!")
            self._database_gway.execute(
                query=_build_insert_query(response_builder)
            )

# =========== RUN METHOD
    def run(self):
        _LOGGER.info(constants.START_MESSAGE)

        # TODO: switch API keys based on the number of requests done.

        opwmap_key = self._api_keys[0]
        _LOGGER.debug("API key in use for connecting to server => %s" % repr(opwmap_key))

        self._delete_forecast_measures()

        try:
            for city in self._cached_cities:
                self._safe_insert_weather_of(
                    api_key=opwmap_key.key_value,
                    city=city
                )
            _LOGGER.info(constants.END_MESSAGE)
        except Exception as err:
            if not isinstance(err, SystemExit) and not isinstance(err, KeyboardInterrupt):
                if self._cached_hourly_forecast and self._cached_daily_forecast:
                    self._database_gway.execute(
                        query=_build_insert_cached_forecast_records_query(
                            hourly=self._cached_hourly_forecast,
                            daily=self._cached_daily_forecast)
                    )
            raise

