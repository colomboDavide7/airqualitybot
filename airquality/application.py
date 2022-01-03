######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 19:05
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
from airquality.environment import Environment
from airquality.usecase.add_places import AddPlaces
from airquality.usecase.add_station_measures import AddThingspeakMeasures
from airquality.usecase.add_fixed_sensors import AddPurpleairFixedSensors
from airquality.usecase.add_mobile_measures import AddAtmotubeMeasures
from airquality.database.gateway import DatabaseGateway
from airquality.database.adapter import Psycopg2Adapter


class WrongUsageError(Exception):
    """
    An *Exception* that defines the type of error raised when the application is used in the wrong way.
    """

    def __init__(self, cause: str):
        self.cause = cause

    def __repr__(self):
        return f"{type(self).__name__}(cause={self.cause})"


class Application(object):
    """
    An *object* that implements the context manager interface and defines the *main()* method, application entry point.
    All the relevant Exceptions are caught at higher level by this class and logged.
    """

    def __init__(self, env: Environment):
        self.args = sys.argv[1:]
        self.env = env

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == WrongUsageError:
            print(repr(exc_val))
            print(self.env.program_usage_msg)
            sys.exit(1)

    def main(self):
        """
        The application entry point method.
        """

        if not self.args:
            raise WrongUsageError("expected at least one argument!")

        personality = self.args[0]
        if personality not in self.env.valid_personalities:
            raise WrongUsageError("invalid personality!")

        with Psycopg2Adapter(
                dbname=self.env.dbname,
                user=self.env.user,
                password=self.env.password,
                host=self.env.host,
                port=self.env.port
        ) as dbadapter:
            print(f"RUNNING {personality}...")
            if personality == 'purpleair':
                AddPurpleairFixedSensors(
                    output_gateway=DatabaseGateway(dbadapter=dbadapter),
                    input_url_template=self.env.url_template(personality)
                ).run()

            elif personality == 'atmotube':
                AddAtmotubeMeasures(
                    output_gateway=DatabaseGateway(dbadapter=dbadapter),
                    input_url_template=self.env.url_template(personality)
                    ).run()

            elif personality == 'thingspeak':
                AddThingspeakMeasures(
                    output_gateway=DatabaseGateway(dbadapter=dbadapter),
                    input_url_template=self.env.url_template(personality)
                ).run()
            elif personality == 'geonames':
                AddPlaces(
                    output_gateway=DatabaseGateway(dbadapter=dbadapter),
                    input_dir_path=self.env.input_dir_of(personality)
                ).run()
            print("finish!")
