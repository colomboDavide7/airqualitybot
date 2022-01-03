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


class AddWeatherData(object):

    def __init__(self, output_gateway: DatabaseGateway, input_url_template: str):
        self.output_gateway = output_gateway
        self.input_url_template = input_url_template

    @property
    def measure_param(self) -> Dict[str, int]:
        return self.output_gateway.get_measure_param_owned_by(owner="openweathermap")

    @property
    def service_param(self) -> List[ServiceParam]:
        return self.output_gateway.get_service_apiparam_of(service_name="openweathermap")

    def run(self):
        measure_param = self.measure_param
        print(repr(measure_param))
        for param in self.service_param:
            print(repr(param))
