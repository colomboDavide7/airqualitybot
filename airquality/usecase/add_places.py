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
import airquality.environment as environ
from airquality.database.gateway import DatabaseGateway
from airquality.core.apidata_builder import GeonamesDataBuilder
from airquality.core.request_builder import AddPlacesRequestBuilder
from airquality.core.request_validator import AddPlacesRequestValidator
from airquality.core.response_builder import AddPlacesResponseBuilder


class AddPlaces(object):

    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._environ = environ.get_environ()
        self._logger = logging.getLogger(__name__)

    def _resource_dir(self):
        return self._environ.input_dir_of(
            personality='geonames'
        )

    @property
    def filenames(self) -> Set[str]:
        return {f for f in listdir(self._resource_dir()) if isfile(self.fullpath(f)) and not f.startswith('.')}

    @property
    def service_id(self) -> int:
        return self._database_gway.query_service_id_from_name(service_name='geonames')

    def poscodes_of(self, country_code: str) -> Set[str]:
        return self._database_gway.query_poscodes_of_country(country_code=country_code)

    def fullpath(self, filename: str) -> str:
        return join(self._resource_dir(), filename)

    def run(self) -> None:
        service_id = self.service_id
        self._logger.debug("service id in use for fetching data => %d" % service_id)

        for f in self.filenames:
            self._logger.debug("reading geonames data from => '%s'" % f)

            country_code = f.split('.')[0]
            database_pcodes = self.poscodes_of(country_code=country_code)
            self._logger.debug(
                "found #%d database postal codes for country => '%s'" % (len(database_pcodes), country_code)
            )

            datamodel_builder = GeonamesDataBuilder(filepath=self.fullpath(f))
            self._logger.debug("found #%d file lines" % len(datamodel_builder))

            request_builder = AddPlacesRequestBuilder(datamodels=datamodel_builder)
            self._logger.debug("found #%d requests" % len(request_builder))

            validator = AddPlacesRequestValidator(
                requests=request_builder,
                existing_poscodes=database_pcodes
            )
            self._logger.debug("found #%d valid requests" % len(validator))

            response_builder = AddPlacesResponseBuilder(
                requests=validator,
                service_id=service_id
            )
            self._logger.debug("found #%d responses" % len(response_builder))

            if response_builder:
                self._logger.debug("inserting new places!")
                self._database_gway.insert_places(response_builder)
