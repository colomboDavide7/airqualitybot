######################################################
#
# Author: Davide Colombo
# Date: 03/01/22 20:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, List
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.service_param import ServiceParam
from airquality.core.apidata_builder import OpenWeatherMapAPIDataBuilder, WeatherCityDataBuilder
from airquality.core.request_builder import AddOpenWeatherMapDataRequestBuilder
from airquality.core.response_builder import AddOpenWeatherMapDataResponseBuilder


class AddWeatherData(object):

    def __init__(self, output_gateway: DatabaseGateway, input_url_template: str):
        self.output_gateway = output_gateway
        self.input_url_template = input_url_template

    @property
    def service_param(self) -> List[ServiceParam]:
        return self.output_gateway.get_service_apiparam_of(service_name="openweathermap")

    @property
    def weather_map(self) -> Dict[int, Dict[str, int]]:
        return self.output_gateway.get_weather_conditions()

    @property
    def service_id(self):
        return self.output_gateway.get_service_id_from_name(service_name="openweathermap")

    def run(self):
        for param in self.service_param:
            print(repr(param))

            cities = WeatherCityDataBuilder(filepath="resources/weather_cities.json")
            for city in cities:
                print(repr(city))
                geoarea_info = self.output_gateway.get_geolocation_of(city=city)

                pre_formatted_url = self.input_url_template.format(
                    api_key=param.api_key, lat=geoarea_info.latitude, lon=geoarea_info.longitude
                )
                datamodel_builder = OpenWeatherMapAPIDataBuilder(url=pre_formatted_url)
                print(f"found #{len(datamodel_builder)} API data")

                request_builder = AddOpenWeatherMapDataRequestBuilder(datamodels=datamodel_builder, weather_map=self.weather_map)
                print(f"found #{len(request_builder)} requests")

                validator = request_builder

                response_builder = AddOpenWeatherMapDataResponseBuilder(
                    requests=validator, service_id=self.service_id, geoarea_id=geoarea_info.geoarea_id
                )
                print(f"found #{len(response_builder)} responses")

                if response_builder:
                    print("inserting new weather data!")
                    self.output_gateway.insert_weather_data(responses=response_builder)
