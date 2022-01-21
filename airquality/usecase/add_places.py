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

    def __init__(self, input_dir: str, output_gateway: DatabaseGateway):
        self._input_dir = input_dir
        self._database_gway = output_gateway
        self._logger = logging.getLogger(__name__)

    @property
    def filenames(self) -> Set[str]:
        return {f for f in listdir(self._input_dir) if isfile(self.fullpath(f)) and not f.startswith('.')}

    @property
    def service_id(self) -> int:
        return self._database_gway.query_service_id_from_name(service_name='geonames')

    def poscodes_of(self, country_code: str) -> Set[str]:
        return self._database_gway.query_poscodes_of_country(country_code=country_code)

    def fullpath(self, filename: str) -> str:
        return join(self._input_dir, filename)

    def run(self) -> None:
        service_id = self.service_id
        for f in self.filenames:
            self._logger.info("filename => %s" % f)

            country_code = f.split('.')[0]
            database_pcodes = self.poscodes_of(country_code=country_code)
            self._logger.info("queried #%d postal codes of country='%s'" % (len(database_pcodes), country_code))

            datamodel_builder = GeonamesDataBuilder(
                filepath=self.fullpath(f)
            )
            self._logger.info("found #%d file lines" % len(datamodel_builder))

            request_builder = AddPlacesRequestBuilder(
                datamodels=datamodel_builder
            )
            self._logger.info("found #%d requests" % len(request_builder))

            validator = AddPlacesRequestValidator(
                requests=request_builder,
                existing_poscodes=database_pcodes
            )
            self._logger.info("found #%d valid requests" % len(validator))

            response_builder = AddPlacesResponseBuilder(
                requests=validator,
                service_id=service_id
            )
            self._logger.info("found #%d responses" % len(response_builder))

            if response_builder:
                self._logger.info("inserting new places!")
                self._database_gway.insert_places(response_builder)
