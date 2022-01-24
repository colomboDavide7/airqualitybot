######################################################
#
# Author: Davide Colombo
# Date: 03/01/22 20:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
from typing import Dict, List
import airquality.environment as environ
from airquality.extra.timest import Timest
from airquality.datamodel.apidata import WeatherCityData
from airquality.database.gateway import DatabaseGateway
from airquality.url.api_server_wrap import APIServerWrapper
from airquality.datamodel.openweathermap_key import OpenweathermapKey
from airquality.core.request_builder import AddOpenWeatherMapDataRequestBuilder
from airquality.core.response_builder import AddOpenWeatherMapDataResponseBuilder
from airquality.core.apidata_builder import OpenWeatherMapAPIDataBuilder, WeatherCityDataBuilder


class AddWeatherData(object):
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

    def __init__(
        self,
        database_gway: DatabaseGateway,
        server_wrap: APIServerWrapper,
        timest: Timest
    ):
        self._timest = timest
        self._server_wrap = server_wrap
        self._database_gway = database_gway
        self._environ = environ.get_environ()
        self._logger = logging.getLogger(__name__)
        self._cached_url_template = ""
        self._cached_weather_map = {}
        self._cached_cities = None

    @property
    def cities_of_interest(self):
        if self._cached_cities is None:
            self._cached_cities = WeatherCityDataBuilder(filepath='resources/weather_cities.json')
        return self._cached_cities

    @property
    def openweathermap_keys(self) -> List[OpenweathermapKey]:
        return self._database_gway.query_openweathermap_keys()

    @property
    def weather_map(self) -> Dict[int, Dict[str, int]]:
        if not self._cached_weather_map:
            rows = self._database_gway.query_weather_conditions()
            weather_map = {code: {} for id_, code, icon in rows}
            for id_, code, icon in rows:
                weather_map[code][icon] = id_
            self._cached_weather_map = weather_map
        return self._cached_weather_map

    def _url_template(self) -> str:
        if not self._cached_url_template:
            self._cached_url_template = self._environ.url_template(personality='openweathermap')
        return self._cached_url_template

    def _delete_forecast_measures(self):
        """
        This method should be called at the beginning of the run method and NOT WITHIN any loop, otherwise
        every loop the measures are deleted and only those of the last city are kept in the database.
        """
        self._logger.warning("deleting all the hourly weather forecast data")
        self._database_gway.delete_all_from_hourly_weather_forecast()
        self._logger.warning("deleting all the daily weather forecast data")
        self._database_gway.delete_all_from_daily_weather_forecast()

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
            geoarea_info = self._database_gway.query_geolocation_of(city=city)
            self._logger.debug("found database correspondence for this city => %s" % repr(geoarea_info))

            pre_formatted_url = self._url_template().format(
                api_key=api_key,
                lat=geoarea_info.latitude,
                lon=geoarea_info.longitude
            )
            self._logger.debug(f"fetching weather data at => {pre_formatted_url}")

            service_jresp = self._server_wrap.json(url=pre_formatted_url)
            self._logger.debug("successfully get server response!!!")

            datamodel_builder = OpenWeatherMapAPIDataBuilder(json_response=service_jresp)
            self._logger.debug("found #%d API data" % len(datamodel_builder))

            request_builder = AddOpenWeatherMapDataRequestBuilder(
                datamodels=datamodel_builder,
                weather_map=self.weather_map,
                timest=self._timest
            )
            self._logger.debug("found #%d requests" % len(request_builder))

            response_builder = AddOpenWeatherMapDataResponseBuilder(
                requests=request_builder,
                geoarea_id=geoarea_info.geoarea_id
            )
            self._logger.debug("found #%d responses" % len(response_builder))

            if response_builder:
                self._logger.debug("inserting new weather data!")
                self._database_gway.insert_weather_data(responses=response_builder)

        except ValueError as err:
            self._logger.exception(err)

# =========== RUN METHOD
    def run(self):
        opwmap_key = self.openweathermap_keys[0]       # for now, we use only the first API key
        self._logger.debug("API key in use for connecting to server => %s" % repr(opwmap_key))

        self._delete_forecast_measures()

        for city in self.cities_of_interest:
            self._logger.debug("downloading weather data for => %s" % repr(city))
            self._safe_insert_weather_of(
                api_key=opwmap_key.key_value,
                city=city
            )
