######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 11:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from airquality.parser.datetime_parser import DatetimeParser
from airquality.geom.postgis_geometry import PostGISPointFactory
from airquality.dispatcher.sql_dispatcher_initialize import InitializePacketSQLDispatcher
from airquality.container.sql_container import APIParamSQLContainer, GeoSQLContainer, SensorSQLContainer
from airquality.container.sql_container_composition import APIParamSQLContainerComposition


################################ CONTAINER FACTORY ################################
class InitializeContainerFactory:

    @staticmethod
    def make_container(bot_personality: str, packet: Dict[str, Any], sensor_id: int) -> InitializePacketSQLDispatcher:

        if bot_personality == 'purpleair':

            # sensor container
            sensor_name = f"{packet['name']} ({packet['sensor_index']})"
            sensor_type = bot_personality
            sensor_container = SensorSQLContainer(sensor_name=sensor_name, sensor_type=sensor_type)

            # api param container composition
            api_container = [APIParamSQLContainer(param_name='primary_id_a', param_value=packet['primary_id_a'], sensor_id=sensor_id),
                             APIParamSQLContainer(param_name='primary_id_b', param_value=packet['primary_id_b'], sensor_id=sensor_id),
                             APIParamSQLContainer(param_name='primary_key_a', param_value=packet['primary_key_a'], sensor_id=sensor_id),
                             APIParamSQLContainer(param_name='primary_key_b', param_value=packet['primary_key_b'], sensor_id=sensor_id),
                             APIParamSQLContainer(param_name='secondary_id_a', param_value=packet['secondary_id_a'], sensor_id=sensor_id),
                             APIParamSQLContainer(param_name='secondary_id_b', param_value=packet['secondary_id_b'], sensor_id=sensor_id),
                             APIParamSQLContainer(param_name='secondary_key_a', param_value=packet['secondary_key_a'], sensor_id=sensor_id),
                             APIParamSQLContainer(param_name='secondary_key_b', param_value=packet['secondary_key_b'], sensor_id=sensor_id),
                             APIParamSQLContainer(param_name='primary_timestamp_a', param_value='2018-01-01 00:00:00', sensor_id=sensor_id),
                             APIParamSQLContainer(param_name='primary_timestamp_b', param_value='2018-01-01 00:00:00', sensor_id=sensor_id),
                             APIParamSQLContainer(param_name='secondary_timestamp_a', param_value='2018-01-01 00:00:00', sensor_id=sensor_id),
                             APIParamSQLContainer(param_name='secondary_timestamp_b', param_value='2018-01-01 00:00:00', sensor_id=sensor_id)]

            api_composition = APIParamSQLContainerComposition(children=api_container)

            # geolocation
            point = PostGISPointFactory(lat=packet['latitude'], lng=packet['longitude']).create_geometry()
            geometry = point.get_database_string()
            timestamp = DatetimeParser.current_sqltimestamp()
            geo_container = GeoSQLContainer(sensor_id=sensor_id, timestamp=timestamp, geometry=geometry)

            return InitializePacketSQLDispatcher(containers=[geo_container, api_composition, sensor_container])

        else:
            raise SystemExit(
                f"{InitializeContainerFactory.__name__}: cannot instantiate {InitializePacketSQLDispatcher.__name__} "
                f"instance for personality='{bot_personality}'.")
