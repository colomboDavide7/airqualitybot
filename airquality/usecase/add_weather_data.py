######################################################
#
# Author: Davide Colombo
# Date: 03/01/22 20:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
from typing import Dict, List
from airquality.database.gateway import DatabaseGateway
from airquality.url.api_server_wrap import APIServerWrapper
from airquality.datamodel.service_param import ServiceParam
from airquality.core.apidata_builder import OpenWeatherMapAPIDataBuilder, WeatherCityDataBuilder
from airquality.core.request_builder import AddOpenWeatherMapDataRequestBuilder
from airquality.core.response_builder import AddOpenWeatherMapDataResponseBuilder


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

    def __init__(self, database_gway: DatabaseGateway, server_wrap: APIServerWrapper, input_url_template: str):
        self._database_gway = database_gway
        self._server_wrap = server_wrap
        self.input_url_template = input_url_template
        self._cached_weather_map = {}
        self._logger = logging.getLogger(__name__)

    @property
    def service_param(self) -> List[ServiceParam]:
        return self._database_gway.get_service_apiparam_of(service_name="openweathermap")

    @property
    def weather_map(self) -> Dict[int, Dict[str, int]]:
        if not self._cached_weather_map:
            rows = self._database_gway.query_weather_conditions()
            weather_map = {code: {} for id_, code, icon in rows}
            for id_, code, icon in rows:
                weather_map[code][icon] = id_
            self._cached_weather_map = weather_map
        return self._cached_weather_map

    @property
    def service_id(self):
        return self._database_gway.get_service_id_from_name(service_name="openweathermap")

    def run(self):
        for param in self.service_param:
            self._logger.debug("service => %s" % repr(param))

            cities = WeatherCityDataBuilder(filepath="resources/weather_cities.json")
            for city in cities:
                self._logger.debug("city => %s" % repr(city))

                geoarea_info = self._database_gway.query_geolocation_of(city=city)
                self._logger.debug("geoarea_info => %s" % repr(geoarea_info))

                pre_formatted_url = self.input_url_template.format(
                    api_key=param.api_key, lat=geoarea_info.latitude, lon=geoarea_info.longitude
                )

                service_jresp = self._server_wrap.json(url=pre_formatted_url)
                self._logger.debug("successfully get service response!!!")

                datamodel_builder = OpenWeatherMapAPIDataBuilder(json_response=service_jresp)
                self._logger.debug("found #%d API data" % len(datamodel_builder))

                request_builder = AddOpenWeatherMapDataRequestBuilder(
                    datamodels=datamodel_builder, weather_map=self.weather_map
                )
                self._logger.debug("found #%d requests" % len(request_builder))

                response_builder = AddOpenWeatherMapDataResponseBuilder(
                    requests=request_builder, service_id=self.service_id, geoarea_id=geoarea_info.geoarea_id
                )
                self._logger.debug("found #%d responses" % len(response_builder))

                if response_builder:
                    self._logger.warning("deleting all the hourly weather forecast data")
                    self._database_gway.delete_all_from_hourly_weather_forecast()
                    self._logger.warning("deleting all the daily weather forecast data")
                    self._database_gway.delete_all_from_daily_weather_forecast()
                    self._logger.debug("inserting new weather data!")
                    self._database_gway.insert_weather_data(responses=response_builder)
