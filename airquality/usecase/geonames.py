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
from os.path import isfile, join
import airquality.usecase as constants
from airquality.usecase.abc import UsecaseABC
from airquality.extra.decorator import log_context
from airquality.database.gateway import DatabaseGateway
from airquality.iterables.fromfile import GeonamesIterableDatamodels
from airquality.iterables.requests import GeonamesIterableRequests
from airquality.iterables.validator import PlaceIterableValidRequests
from airquality.iterables.responses import AddPlaceIterableResponses


class Geonames(UsecaseABC):
    """
    A class that implements the *UsecaseABC* and defines the business rules for reading, transforming and validate
    the geonames country files.
    """

    def __init__(self, database_gway: DatabaseGateway):
        self._database_gway = database_gway
        self._root_dir = _ENVIRON.input_dir_of(personality='geonames')
        self._filenames = {f for f in listdir(self._root_dir) if isfile(join(self._root_dir, f)) and not f.startswith('.')}

    @log_context(logger_name=__name__, header=constants.START_MESSAGE, teardown=constants.END_MESSAGE)
    def execute(self) -> None:
        for fname in self._filenames:
            _LOGGER.debug("COUNTRY FILE => '%s'" % fname)
            country_code = fname.split('.')[0]
            database_pcodes = self._database_gway.query_poscodes_of_country(country_code=country_code)
            datamodels = GeonamesIterableDatamodels(filepath=join(self._root_dir, fname))
            requests = GeonamesIterableRequests(datamodels=datamodels)
            valid_requests = PlaceIterableValidRequests(requests=requests, postcodes2remove=database_pcodes)
            if not valid_requests:
                _LOGGER.debug('no valid postal codes found.')
                continue

            responses = AddPlaceIterableResponses(requests=valid_requests)
            self._database_gway.execute(query=responses.query())
            _LOGGER.debug('inserted %d/%d places.' % (len(valid_requests), len(datamodels)))
