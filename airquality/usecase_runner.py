######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 10:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import abstractmethod
from airquality.environment import Environment
from airquality.database.adapter import Psycopg2Adapter
from airquality.database.gateway import DatabaseGateway


class UsecaseRunner(object):
    """
    An *object* that defines a common interface for running the application UseCases.
    """

    def __init__(self, env: Environment, personality: str):
        self.env = env
        self.personality = personality

    @abstractmethod
    def run(self):
        pass


from airquality.core.apidata_builder import PurpleairAPIDataBuilder
from airquality.usecase.add_fixed_sensors import AddFixedSensors


class AddFixedSensorsRunner(UsecaseRunner):
    """
    A *UsecaseRunner* that defines how to run an *AddFixedSensors* UseCase.
    """

    def run(self):
        with Psycopg2Adapter(dbname=self.env.dbname,
                             user=self.env.user,
                             password=self.env.password,
                             host=self.env.host,
                             port=self.env.port) as dbadapter:

            gateway = DatabaseGateway(dbadapter=dbadapter)
            start_sensor_id = gateway.get_max_sensor_id_plus_one()
            existing_names = gateway.get_existing_sensor_names_of_type(sensor_type=self.personality)
            datamodels = PurpleairAPIDataBuilder(url=self.env.url_template(personality=self.personality))
            AddFixedSensors(
                output_gateway=gateway,
                existing_names=existing_names,
                start_sensor_id=start_sensor_id
            ).process(datamodels=datamodels)


from airquality.url.timeiter_url import AtmotubeTimeIterableURL
from airquality.core.apidata_builder import AtmotubeAPIDataBuilder
from airquality.usecase.add_mobile_measures import AddMobileMeasures


class AddMobileMeasuresRunner(UsecaseRunner):
    """
    A *UsecaseRunner* that defines how to run an *AddMobileMeasures* UseCase.
    """

    def run(self):
        with Psycopg2Adapter(dbname=self.env.dbname,
                             user=self.env.user,
                             password=self.env.password,
                             host=self.env.host,
                             port=self.env.port) as dbadapter:

            gateway = DatabaseGateway(dbadapter=dbadapter)
            url_template = self.env.url_template(personality=self.personality)
            code2id = gateway.get_measure_param_owned_by(owner=self.personality)
            apiparam = gateway.get_apiparam_of_type(sensor_type=self.personality)
            for param in apiparam:
                pre_formatted_url = url_template.format(api_key=param.api_key, api_id=param.api_id, api_fmt="json")
                urls = AtmotubeTimeIterableURL(url=pre_formatted_url, begin=param.last_acquisition)
                for url in urls:
                    start_packet_id = gateway.get_max_mobile_packet_id_plus_one()
                    filter_ts = gateway.get_last_acquisition_of_sensor_channel(
                        sensor_id=param.sensor_id,
                        ch_name=param.ch_name
                    )
                    AddMobileMeasures(
                        output_gateway=gateway,
                        start_packet_id=start_packet_id,
                        sensor_id=param.sensor_id,
                        ch_name=param.ch_name,
                        filter_ts=filter_ts,
                        code2id=code2id
                    ).process(datamodels=AtmotubeAPIDataBuilder(url=url))
