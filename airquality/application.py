######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 19:05
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
import logging.config
import airquality.environment as environ
from airquality.usecase.add_geonames_places import AddGeonamesPlaces
from airquality.usecase.add_purpleair_measures import AddPurpleairMeasures
from airquality.usecase.add_purpleair_sensors import AddPurpleairFixedSensors
from airquality.usecase.add_atmotube_measures import AddAtmotubeMeasures
from airquality.usecase.update_purpleair_locations import UpdatePurpleairLocation
from airquality.usecase.add_weather_data import AddWeatherData
from airquality.database.gateway import DatabaseGateway
from airquality.database.adapter import Psycopg2Adapter


_LOGGER = logging.getLogger(__name__)
_ENVIRON = environ.get_environ()


class WrongUsageError(Exception):
    """
    A subclass of Exception that is raised to signal that the program is used in a wrong way.
    """
    pass


class Application(object):
    def __init__(self):
        self._args = sys.argv[1:]
        self._exit_code = 0

# =========== CONTEXT MANAGER INTERFACE
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._exit_code = 1
            _LOGGER.exception(exc_val)
            if exc_type == WrongUsageError:
                print(_ENVIRON.program_usage_msg)
        _LOGGER.debug("finish with exit code %d" % self._exit_code)
        logging.shutdown()
        sys.exit(self._exit_code)

# =========== MAIN METHOD
    def main(self):
        if not self._args:
            raise WrongUsageError("[FATAL]: missing 'personality' argument!!!")

        personality = self._args[0]
        if personality not in _ENVIRON.valid_personalities:
            raise WrongUsageError("[FATAL]: invalid 'personality' argument!!!")

        with Psycopg2Adapter(
            dbname=_ENVIRON.dbname,
            user=_ENVIRON.dbuser,
            password=_ENVIRON.dbpwd,
            host=_ENVIRON.dbhost,
            port=_ENVIRON.dbport
        ) as psycopg2_adapt:
            database_gway = DatabaseGateway(database_adapt=psycopg2_adapt)
            if personality == 'purpleair':
                AddPurpleairFixedSensors(database_gway=database_gway).run()
            elif personality == 'atmotube':
                AddAtmotubeMeasures(database_gway=database_gway).run()
            elif personality == 'thingspeak':
                AddPurpleairMeasures(database_gway=database_gway).run()
            elif personality == 'geonames':
                AddGeonamesPlaces(database_gway=database_gway).run()
            elif personality == 'openweathermap':
                AddWeatherData(database_gway=database_gway).run()
            elif personality == 'purp_update':
                UpdatePurpleairLocation(database_gway=database_gway).run()
