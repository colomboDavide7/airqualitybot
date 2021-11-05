######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 11:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
from dataclasses import dataclass
from airquality.container.api_param_container import APIParamContainer


@dataclass
class InitializeContainer:
    database_sensor_name: str
    sensor_type: str
    api_param_container: List[APIParamContainer]


# @dataclass
# class InitializeContainerPurpleair(InitializeContainer):
#     name: str
#     sensor_index: str
#     primary_id_a: str
#     primary_id_b: str
#     secondary_id_a: str
#     secondary_id_b: str
#     primary_key_a: str
#     primary_key_b: str
#     secondary_key_a: str
#     secondary_key_b: str
#     latitude: str
#     longitude: str
#     altitude: str
#
#     def __post_init__(self):
#         self.database_sensor_name = f"{self.name} ({self.sensor_index})"
#         self.sensor_type = 'purpleair'
#         self.api_param_container = [APIParamContainer(param_name='primary_id_a', param_value=self.primary_id_a),
#                                     APIParamContainer(param_name='primary_id_b', param_value=self.primary_id_b),
#                                     APIParamContainer(param_name='primary_key_a', param_value=self.primary_key_a),
#                                     APIParamContainer(param_name='primary_key_b', param_value=self.primary_key_b),
#                                     APIParamContainer(param_name='secondary_id_a', param_value=self.secondary_id_a),
#                                     APIParamContainer(param_name='secondary_id_b', param_value=self.secondary_id_b),
#                                     APIParamContainer(param_name='secondary_key_a', param_value=self.secondary_key_a),
#                                     APIParamContainer(param_name='secondary_key_b', param_value=self.secondary_key_b),
#                                     APIParamContainer(param_name='primary_timestamp_a', param_value='null'),
#                                     APIParamContainer(param_name='primary_timestamp_b', param_value='null'),
#                                     APIParamContainer(param_name='secondary_timestamp_a', param_value='null'),
#                                     APIParamContainer(param_name='secondary_timestamp_b', param_value='null')]


################################ CONTAINER FACTORY ################################
class InitializeContainerFactory:

    @staticmethod
    def make_container(bot_personality: str, parameters: Dict[str, Any]) -> InitializeContainer:
        if bot_personality == 'purpleair':
            database_sensor_name = f"{parameters['name']}' ({parameters['sensor_index']})"
            sensor_type = 'purpleair'
            api_container = [APIParamContainer(param_name='primary_id_a', param_value=parameters['primary_id_a']),
                             APIParamContainer(param_name='primary_id_b', param_value=parameters['primary_id_b']),
                             APIParamContainer(param_name='primary_key_a', param_value=parameters['primary_key_a']),
                             APIParamContainer(param_name='primary_key_b', param_value=parameters['primary_key_b']),
                             APIParamContainer(param_name='secondary_id_a', param_value=parameters['secondary_id_a']),
                             APIParamContainer(param_name='secondary_id_b', param_value=parameters['secondary_id_b']),
                             APIParamContainer(param_name='secondary_key_a', param_value=parameters['secondary_key_a']),
                             APIParamContainer(param_name='secondary_key_b', param_value=parameters['secondary_key_b']),
                             APIParamContainer(param_name='primary_timestamp_a', param_value='null'),
                             APIParamContainer(param_name='primary_timestamp_b', param_value='null'),
                             APIParamContainer(param_name='secondary_timestamp_a', param_value='null'),
                             APIParamContainer(param_name='secondary_timestamp_b', param_value='null')]

            return InitializeContainer(database_sensor_name=database_sensor_name,
                                       sensor_type=sensor_type,
                                       api_param_container=api_container)
        else:
            raise SystemExit(
                f"{InitializeContainerFactory.__name__}: cannot instantiate {InitializeContainer.__name__} "
                f"instance for personality='{bot_personality}'.")
