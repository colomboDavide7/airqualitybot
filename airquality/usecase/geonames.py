######################################################
#
# Author: Davide Colombo
# Date: 02/01/22 17:16
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
import airquality.environment as environ

_ENVIRON = environ.get_environ()
_LOGGER = logging.getLogger(__name__)

######################################################
from os import listdir
from typing import Set
from os.path import isfile, join
import airquality.usecase as constants
from airquality.usecase.abc import UsecaseABC
from airquality.database.gateway import DatabaseGateway
from airquality.iterables.fromfile import GeonamesIterableDatamodels
from airquality.iterables.requests import GeonamesIterableRequests
from airquality.iterables.validator import AddPlaceRequestValidator
from airquality.iterables.responses import AddPlaceIterableResponses


def _resource_dir():
    return _ENVIRON.input_dir_of(personality='geonames')


def _fullpath(filename: str) -> str:
    return join(_resource_dir(), filename)


def _build_insert_query(response_builder: AddPlaceIterableResponses) -> str:
    return "INSERT INTO level0_raw.geographical_area " \
           "(postal_code, country_code, place_name, province, state, geom) " \
           f"VALUES {','.join(resp.place_record for resp in response_builder)};"


class AddGeonamesPlaces(UsecaseABC):
    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._filenames = {f for f in listdir(_resource_dir()) if isfile(_fullpath(f)) and not f.startswith('.')}

    def _poscodes_of(self, country_code: str) -> Set[str]:
        return self._database_gway.query_poscodes_of_country(country_code=country_code)

    def run(self) -> None:
        _LOGGER.info(constants.START_MESSAGE)
        for f in self._filenames:
            _LOGGER.debug("reading geonames data from => '%s'" % f)

            country_code = f.split('.')[0]
            database_pcodes = self._poscodes_of(country_code=country_code)
            _LOGGER.debug("found #%d database postal codes for country => '%s'"
                          % (len(database_pcodes), country_code))

            datamodel_builder = GeonamesIterableDatamodels(filepath=_fullpath(f))
            _LOGGER.debug("found #%d file lines" % len(datamodel_builder))

            request_builder = GeonamesIterableRequests(datamodels=datamodel_builder)
            _LOGGER.debug("found #%d requests" % len(request_builder))

            validator = AddPlaceRequestValidator(
                requests=request_builder,
                postcodes2remove=database_pcodes
            )
            _LOGGER.debug("found #%d valid requests" % len(validator))

            response_builder = AddPlaceIterableResponses(requests=validator)
            _LOGGER.debug("found #%d responses" % len(response_builder))

            if len(response_builder) > 0:
                _LOGGER.debug("inserting new places!")
                self._database_gway.execute(
                    query=_build_insert_query(response_builder)
                )
        _LOGGER.info(constants.END_MESSAGE)
