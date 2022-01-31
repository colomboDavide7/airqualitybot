######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 19:05
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
import logging
import airquality.environment as environ

_ROOT_LOGGER = logging.getLogger()
_ENVIRON = environ.get_environ()
_SYS_ARGS = sys.argv[1:]

######################################################
from airquality.usecase.add_geonames_places import AddGeonamesPlaces
from airquality.usecase.add_purpleair_measures import AddPurpleairMeasures
from airquality.usecase.add_purpleair_sensors import AddPurpleairFixedSensors
from airquality.usecase.add_atmotube_measures import AddAtmotubeMeasures
from airquality.usecase.update_purpleair_locations import UpdatePurpleairLocation
from airquality.usecase.add_weather_data import AddWeatherData
from airquality.database.gateway import DatabaseGateway
from airquality.database.adapter import Psycopg2Adapter


def _raise(cause: str):
    _ROOT_LOGGER.exception(cause, exc_info=False)
    raise ValueError(cause) from None


class Application(object):
    def __init__(self):
        self._exit_code = 0
        if not _SYS_ARGS:
            self._exit_code = 1
            _raise(cause="Expected at least one argument")

        self._personality = _SYS_ARGS[0]
        if self._personality not in _ENVIRON.valid_personalities:
            self._exit_code = 2
            _raise(cause=f"Expected '%s' to be one of %s" % (self._personality, _ENVIRON.valid_personalities))

# =========== CONTEXT MANAGER INTERFACE
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._exit_code = 3
            _ROOT_LOGGER.exception(exc_val)
        _ROOT_LOGGER.debug("finish with exit code %d" % self._exit_code)
        logging.shutdown()
        sys.exit(self._exit_code)

# =========== MAIN METHOD
    def main(self):
        with Psycopg2Adapter(
            dbname=_ENVIRON.dbname,
            user=_ENVIRON.dbuser,
            password=_ENVIRON.dbpwd,
            host=_ENVIRON.dbhost,
            port=_ENVIRON.dbport
        ) as database_adapt:
            database_gway = DatabaseGateway(database_adapt=database_adapt)
            if self._personality == 'purpleair':
                AddPurpleairFixedSensors(database_gway=database_gway).run()
            elif self._personality == 'atmotube':
                AddAtmotubeMeasures(database_gway=database_gway).run()
            elif self._personality == 'thingspeak':
                AddPurpleairMeasures(database_gway=database_gway).run()
            elif self._personality == 'geonames':
                AddGeonamesPlaces(database_gway=database_gway).run()
            elif self._personality == 'openweathermap':
                AddWeatherData(database_gway=database_gway).run()
            elif self._personality == 'purp_update':
                UpdatePurpleairLocation(database_gway=database_gway).run()
