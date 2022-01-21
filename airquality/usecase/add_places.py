######################################################
#
# Author: Davide Colombo
# Date: 02/01/22 17:16
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
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
        self.app_logger = logging.getLogger(__name__)

    @property
    def filenames(self) -> Set[str]:
        return {f for f in listdir(self.input_dir_path) if isfile(self.fullpath(f)) and not f.startswith('.')}

    @property
    def service_id(self) -> int:
        return self.output_gateway.query_service_id_from_name(service_name='geonames')

    def poscodes_of(self, country_code: str) -> Set[str]:
        return self.output_gateway.query_poscodes_of_country(country_code=country_code)

    def fullpath(self, filename: str) -> str:
        return join(self.input_dir_path, filename)

    def run(self) -> None:
        service_id = self.service_id
        for f in self.filenames:
            self.app_logger.info("filename => %s" % f)

            datamodel_builder = GeonamesDataBuilder(filepath=self.fullpath(f))
            self.app_logger.info("found #%d file lines" % len(datamodel_builder))

            request_builder = AddPlacesRequestBuilder(datamodels=datamodel_builder)
            self.app_logger.info("found #%d requests" % len(request_builder))

            dbposcodes = self.poscodes_of(country_code=f.split('.')[0])
            self.app_logger.info("found #%d unique database poscodes of country='%s'" % (len(dbposcodes), f.split('.')[0]))

            validator = AddPlacesRequestValidator(requests=request_builder, existing_poscodes=dbposcodes)
            self.app_logger.info("found #%d valid requests" % len(validator))

            response_builder = AddPlacesResponseBuilder(requests=validator, service_id=service_id)
            self.app_logger.info("found #%d responses" % len(response_builder))

            if response_builder:
                self.app_logger.info("inserting new places!")
                self.output_gateway.insert_places(response_builder)
