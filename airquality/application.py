######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 19:05
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import json
import sys
import logging.config
from airquality.environment import Environment
from airquality.usecase.add_places import AddPlaces
from airquality.url.api_server_wrap import APIServerWrapper
from airquality.usecase.add_station_measures import AddThingspeakMeasures
from airquality.usecase.add_fixed_sensors import AddPurpleairFixedSensors
from airquality.usecase.add_mobile_measures import AddAtmotubeMeasures
from airquality.usecase.add_weather_data import AddWeatherData
from airquality.database.gateway import DatabaseGateway
from airquality.database.adapter import Psycopg2Adapter
from airquality.datamodel.timest import purpleair_timest, atmotube_timest, thingspeak_timest, openweathermap_timest


class WrongUsageError(Exception):
    """
    A subclass of Exception that is raised to signal that the program is used in a wrong way.
    """
    pass


class Application(object):
    """
    A class that glues together all the application business classes and prepare the 'ground' for the execution.

    Keyword arguments:
        *env*:                  the Environment instance that defines the boundary interface
                                for interacting with the '.env' file.

    Instance variables:
        *_args*                 the list of command line arguments excluded the very first, i.e. program name.
        *_logger*               the logging.Logger instance that performs auditing about the application run.
        *_exit_code*            the status code at the end of the application: 0 => OK, 1 => Error

    Raises:
        *WrongUsageError*       for stopping the application flow in case of wrong usage.

    This class implements the *context_manager* interface (__enter__, __exit__) in order
    to collect all the exceptions received and safely performs cleanup actions.

    Logger:

    The Logger is configured from the 'logger_conf.json' file, be sure that file exists at the root level.

    """

    def __init__(self, env: Environment):
        with open('logger_conf.json', 'r') as fconf:
            logging.config.dictConfig(json.load(fconf))
        self._args = sys.argv[1:]
        self._env = env
        self._logger = logging.getLogger(__name__)
        self._exit_code = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._exit_code = 1
            self._logger.exception(exc_val)
            if exc_type == WrongUsageError:
                print(self._env.program_usage_msg)
        self._logger.debug("finish with exit code %d" % self._exit_code)
        logging.shutdown()
        sys.exit(self._exit_code)

    def main(self):
        if not self._args:
            raise WrongUsageError("[FATAL]: missing 'personality' argument!!!")

        personality = self._args[0]
        if personality not in self._env.valid_personalities:
            raise WrongUsageError("[FATAL]: invalid 'personality' argument!!!")

        with Psycopg2Adapter(
            dbname=self._env.dbname,
            user=self._env.dbuser,
            password=self._env.dbpwd,
            host=self._env.dbhost,
            port=self._env.dbport
        ) as database_wrap:
            self._logger.debug("running %s" % personality)
            if personality == 'purpleair':
                AddPurpleairFixedSensors(
                    database_gway=DatabaseGateway(database_adapt=database_wrap),
                    server_wrap=APIServerWrapper(),
                    timest=purpleair_timest(),
                    input_url_template=self._env.url_template(personality)
                ).run()

            elif personality == 'atmotube':
                AddAtmotubeMeasures(
                    database_gway=DatabaseGateway(database_adapt=database_wrap),
                    server_wrap=APIServerWrapper(),
                    timest=atmotube_timest(),
                    input_url_template=self._env.url_template(personality)
                ).run()

            elif personality == 'thingspeak':
                AddThingspeakMeasures(
                    database_gway=DatabaseGateway(database_adapt=database_wrap),
                    timest=thingspeak_timest(),
                    server_wrap=APIServerWrapper()
                ).run()
            elif personality == 'geonames':
                AddPlaces(
                    output_gateway=DatabaseGateway(database_adapt=database_wrap),
                    input_dir=self._env.input_dir_of(personality)
                ).run()
            elif personality == 'openweathermap':
                AddWeatherData(
                    database_gway=DatabaseGateway(database_adapt=database_wrap),
                    server_wrap=APIServerWrapper(),
                    timest=openweathermap_timest(),
                    input_url_template=self._env.url_template(personality)
                ).run()
