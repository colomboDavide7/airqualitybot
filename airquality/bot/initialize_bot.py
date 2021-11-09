#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 08:30
# @Description: this script contains the classes for initializing the database with different sensor's data.
#
#################################################
from typing import Dict, Any, List

# IMPORT GLOBAL VARIABLE FROM FETCH MODULE
import airquality.constants.system_constants as sc

# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.api.url_builder import URLBuilder
from airquality.api.urllib_adapter import UrllibAdapter
from airquality.parser.datetime_parser import DatetimeParser
from airquality.geom.postgis_geometry import PostGISGeometry
from airquality.database.db_conn_adapter import ConnectionAdapter
from airquality.adapter.universal_db_adapter import UniversalDatabaseAdapter
from airquality.container.sql_container import GeoSQLContainer, SQLContainerComposition, \
    SensorSQLContainer, APIParamSQLContainer

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, INFO_HEADER, WARNING_HEADER


################################ INITIALIZE BOT ################################
class InitializeBot:

    def __init__(self,
                 dbconn: ConnectionAdapter,
                 file_parser_class,
                 reshaper_class,
                 url_builder_class=URLBuilder,
                 universal_adapter_class=UniversalDatabaseAdapter,
                 geo_sqlcontainer_class=GeoSQLContainer,
                 sensor_sqlcontainer_class=SensorSQLContainer,
                 apiparam_sqlcontainer_class=APIParamSQLContainer,
                 composition_class=SQLContainerComposition,
                 postgis_geom_class=PostGISGeometry):
        self.dbconn = dbconn
        self.file_parser_class = file_parser_class
        self.url_builder_class = url_builder_class
        self.reshaper_class = reshaper_class
        self.geo_sqlcontainer_class = geo_sqlcontainer_class
        self.sensor_sqlcontainer_class = sensor_sqlcontainer_class
        self.apiparam_sqlcontainer_class = apiparam_sqlcontainer_class
        self.composition_class = composition_class
        self.universal_db_adapter_class = universal_adapter_class
        self.postgis_geom_class = postgis_geom_class

    def run(self,
            first_sensor_id: int,
            api_address: str,
            url_param: Dict[str, Any],
            sensor_names: List[str],
            sensor_query: str,
            api_param_query: str,
            sensor_at_location_query: str):

        ################################ API DATA FETCHING ################################
        url_builder = self.url_builder_class(api_address=api_address, parameters=url_param)
        url = url_builder.build_url()
        raw_packets = UrllibAdapter.fetch(url)
        parser = self.file_parser_class()
        parsed_packets = parser.parse(raw_packets)

        ################################ RESHAPE PACKETS ################################
        packet_reshaper = self.reshaper_class()
        reshaped_packets = packet_reshaper.reshape_packet(parsed_packets)

        if reshaped_packets:

            ############################## UNIVERSAL ADAPTER #############################
            universal_db_adapter = self.universal_db_adapter_class()

            universal_db_packets = []
            for universal_packet in reshaped_packets:
                universal_db_packets.append(universal_db_adapter.adapt(universal_packet))

            ############################## FILTER PACKETS #############################
            if sc.DEBUG_MODE:
                print(20 * "=" + " FILTER SENSORS " + 20 * '=')
            filtered_universal_packets = []
            for universal_packet in universal_db_packets:
                if universal_packet['name'] not in sensor_names:
                    filtered_universal_packets.append(universal_packet)
                else:
                    print(f"{WARNING_HEADER} '{universal_packet['name']}' already present...")

            if not filtered_universal_packets:
                print(f"{INFO_HEADER} all sensors are already present into the database.")
                self.dbconn.close_conn()
                return

            if sc.DEBUG_MODE:
                print(20 * "=" + " NEW SENSORS " + 20 * '=')
                for universal_packet in filtered_universal_packets:
                    print(f"{DEBUG_HEADER} name={universal_packet['name']}")

            ############################## CONVERT PARAMETERS INTO SQL CONTAINERS #############################
            temp_sensor_id = first_sensor_id
            geo_containers = []
            sensor_containers = []
            apiparam_containers = []
            for universal_packet in filtered_universal_packets:
                # **************************
                sensor_containers.append(self.sensor_sqlcontainer_class(name=universal_packet['name'],
                                                                        type_= universal_packet['type']))
                # **************************
                # geometry = geom_adapter.adapt(universal_packet)
                geometry = self.postgis_geom_class()
                geom = geometry.get_database_string(universal_packet)
                valid_from = DatetimeParser.current_sqltimestamp()
                geo_containers.append(self.geo_sqlcontainer_class(sensor_id=temp_sensor_id,
                                                                  valid_from=valid_from,
                                                                  geom=geom))
                # **************************
                apiparam_containers.append(self.apiparam_sqlcontainer_class(param_name=universal_packet['param_name'],
                                                                            param_value=universal_packet['param_value'],
                                                                            sensor_id=temp_sensor_id))
                temp_sensor_id += 1

            ############################## COMPOSITION CONTAINERS #############################
            sensor_container_composition = self.composition_class(sensor_containers)
            apiparam_container_composition = self.composition_class(apiparam_containers)
            geo_container_composition = self.composition_class(geo_containers)

            ############################## BUILD THE QUERY FROM CONTAINERS #############################
            query = sensor_container_composition.sql(query=sensor_query)
            query += apiparam_container_composition.sql(query=api_param_query)
            query += geo_container_composition.sql(query=sensor_at_location_query)
            self.dbconn.send(executable_sql_query=query)
        else:
            print(f"{INFO_HEADER} empty packets.")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
