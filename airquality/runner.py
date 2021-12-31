######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 19:05
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
from airquality.environment import Environment
from airquality.database.adapter import Psycopg2Adapter
from airquality.database.gateway import DatabaseGateway
from airquality.core.apidata_builder import PurpleairAPIDataBuilder
from airquality.usecase.add_fixed_sensors import AddFixedSensors

from airquality.url.timeiter_url import AtmotubeTimeIterableURL
from airquality.core.apidata_builder import AtmotubeAPIDataBuilder
from airquality.usecase.add_mobile_measures import AddMobileMeasures


class WrongUsageError(Exception):
    """
    An *Exception* that defines the type of error raised when the application is used in the wrong way.
    """

    def __init__(self, cause: str):
        self.cause = cause

    def __repr__(self):
        return f"{type(self).__name__}(cause={self.cause})"


class Runner(object):
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
        if self.args[0] not in self.env.valid_personalities:
            raise WrongUsageError("invalid personality!")

        if self.args[0] == 'purpleair':
            print("RUNNING Purpleair...")
            # TODO: add context manager for database adapter

            dbadapter = Psycopg2Adapter(
                dbname=self.env.dbname, user=self.env.user, password=self.env.password, host=self.env.host, port=self.env.port
            )

            output_gateway = DatabaseGateway(dbadapter=dbadapter)
            existing_names = output_gateway.get_existing_sensor_names_of_type(sensor_type=self.args[0])
            start_sensor_id = output_gateway.get_max_sensor_id_plus_one()
            datamodels = PurpleairAPIDataBuilder(url=self.env.url_template(personality=self.args[0]))
            AddFixedSensors(
                output_gateway=output_gateway, existing_names=existing_names, start_sensor_id=start_sensor_id
            ).process(datamodels=datamodels)
            print("finish!")

        elif self.args[0] == 'atmotube':
            print("RUNNING Atmotube...")
            # TODO: add context manager for database adapter

            dbadapter = Psycopg2Adapter(
                dbname=self.env.dbname, user=self.env.user, password=self.env.password, host=self.env.host, port=self.env.port
            )
            output_gateway = DatabaseGateway(dbadapter=dbadapter)
            url_template = self.env.url_template(personality=self.args[0])
            code2id = output_gateway.get_measure_param_owned_by(owner=self.args[0])
            apiparam = output_gateway.get_apiparam_of_type(sensor_type=self.args[0])
            print(repr(apiparam))

            for param in apiparam:
                url = url_template.format(api_key=param.api_key, api_id=param.api_id, api_fmt="json")
                urls = AtmotubeTimeIterableURL(url=url, begin=param.last_acquisition)

                for url in urls:
                    start_packet_id = output_gateway.get_max_mobile_packet_id_plus_one()
                    filter_ts = output_gateway.get_last_acquisition_of_sensor_channel(
                        sensor_id=param.sensor_id, ch_name=param.ch_name
                    )
                    AddMobileMeasures(
                        output_gateway=output_gateway, start_packet_id=start_packet_id, filter_ts=filter_ts,
                        code2id=code2id, sensor_id=param.sensor_id, ch_name=param.ch_name
                    ).process(datamodels=AtmotubeAPIDataBuilder(url=url))
