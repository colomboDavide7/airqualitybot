######################################################
#
# Author: Davide Colombo
# Date: 02/01/22 17:16
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from os import listdir
from typing import Set
from os.path import isfile, join
from airquality.database.gateway import DatabaseGateway
from airquality.core.apidata_builder import GeonamesDataBuilder
from airquality.core.request_builder import AddPlacesRequestBuilder
from airquality.core.request_validator import AddPlacesRequestValidator
from airquality.core.response_builder import AddPlacesResponseBuilder


class AddPlaces(object):

    def __init__(self, input_dir_path: str, output_gateway: DatabaseGateway):
        self.input_dir_path = input_dir_path
        self.output_gateway = output_gateway

    @property
    def filenames(self) -> Set[str]:
        return {f for f in listdir(self.input_dir_path) if isfile(self.fullpath(f)) and not f.startswith('.')}

    @property
    def service_id(self) -> int:
        return self.output_gateway.get_service_id_from_name(service_name='geonames')

    def existing_poscodes(self, country_code: str) -> Set[str]:
        return self.output_gateway.get_poscodes_of_country(country_code=country_code)

    def fullpath(self, filename: str) -> str:
        return join(self.input_dir_path, filename)

    def run(self) -> None:
        for f in self.filenames:
            print(f"looking at {f}")

            datamodel_builder = GeonamesDataBuilder(filepath=self.fullpath(f))
            print(f"found #{len(datamodel_builder)} file lines")

            request_builder = AddPlacesRequestBuilder(datamodels=datamodel_builder)
            print(f"found #{len(request_builder)} requests")

            existing_poscodes = self.existing_poscodes(country_code=f.split('.')[0])
            validator = AddPlacesRequestValidator(requests=request_builder, existing_poscodes=existing_poscodes)
            print(f"found #{len(validator)} valid requests")

            response_builder = AddPlacesResponseBuilder(requests=validator, service_id=self.service_id)
            print(f"found #{len(response_builder)} responses")

            if len(response_builder) > 0:
                print(f"commit responses into {self.output_gateway!r}")
                self.output_gateway.insert_places(response_builder)
