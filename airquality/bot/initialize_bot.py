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
from airquality.api.urllib_adapter import UrllibAdapter
from airquality.parser.datetime_parser import DatetimeParser
from airquality.database.db_conn_adapter import ConnectionAdapter
from airquality.adapter.sensor_adapter import SensorAdapter
from airquality.adapter.apiparam_adapter import APIParamAdapter
from airquality.adapter.geom_adapter import GeometryAdapter
from airquality.container.sql_container import GeoSQLContainer, SQLContainerComposition

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, INFO_HEADER


################################ INITIALIZE BOT ################################
class InitializeBot:

    def __init__(self,
                 dbconn: ConnectionAdapter,     # database connection adapter object
                 file_parser_class,             # file parser class for parsing raw file lines
                 url_builder_class,             # builder class for creating the URL for fetching data from API
                 reshaper_class,                # reshaper class for getting the packets in a better shape
                 geom_adapter_class=GeometryAdapter,            # adapter class for geolocation information
                 sensor_adapter_class=SensorAdapter,            # adapter class for sensor information
                 apiparam_adapter_class=APIParamAdapter,        # adapter class for api parameters
                 geo_sqlcontainer_class=GeoSQLContainer,        # container class for converting dict into SQLContainer
                 composition_class=SQLContainerComposition):    # container class that contains a collection of SQLContainer
        self.dbconn = dbconn
        self.file_parser_class = file_parser_class
        self.url_builder_class = url_builder_class
        self.reshaper_class = reshaper_class
        self.geom_adapter_class = geom_adapter_class
        self.sensor_adapter_class = sensor_adapter_class
        self.apiparam_adapter_class = apiparam_adapter_class
        self.geo_sqlcontainer_class = geo_sqlcontainer_class
        self.composition_class = composition_class

    def run(self,
            first_sensor_id: int,               # first sensor id from which starts to count
            url_builder_param: Dict[str, Any],  # parameters for building URL for fetching data from API
            sensor_names: List[str],            # list of the name of the sensor present in database or []
            sensor_query: str,                  # INSERT INTO query for inserting records into 'sensor' table
            api_param_query: str,               # INSERT INTO query for inserting records into 'api_param' table
            sensor_at_location_query: str):     # INSERT INTO query for inserting records into 'sensor_at_location' table

        ################################ API DATA FETCHING ################################
        url_builder = self.url_builder_class()              # instance for building URL
        url = url_builder.build_url(url_builder_param)      # the URL used for fetching data
        raw_packets = UrllibAdapter.fetch(url)              # raw packets fetched from API (json)
        parser = self.file_parser_class()                   # instance for parsing the content
        parsed_packets = parser.parse(raw_packets)          # parsed packets fetched from API (dict)

        ################################ RESHAPE PACKETS ################################
        packet_reshaper = self.reshaper_class()
        reshaped_packets = packet_reshaper.reshape_packet(parsed_packets)

        if reshaped_packets:

            if sc.DEBUG_MODE:
                print(20 * "=" + " RESHAPED PACKETS " + 20 * '=')
                for packet in reshaped_packets:
                    print(30 * '*')
                    for key, val in packet.items():
                        print(f"{DEBUG_HEADER} {key}={val}")

            ############################## ADAPTER FOR CONVERTING DICT INTO CONTAINERS #############################
            geom_adapter = self.geom_adapter_class()
            sensor_adapter = self.sensor_adapter_class()
            apiparam_adapter = self.apiparam_adapter_class()

            ############################## CONVERT PARAMETERS INTO SQL CONTAINERS #############################
            temp_sensor_id = first_sensor_id
            geo_containers = []
            sensor_containers = []
            apiparam_containers = []
            for packet in reshaped_packets:

                # TODO: FILTER CLASS

                # **************************
                sensor_containers.append(sensor_adapter.adapt(packet))
                # **************************
                geometry = geom_adapter.adapt(packet)
                geom = geometry.get_database_string()
                valid_from = DatetimeParser.current_sqltimestamp()
                geo_containers.append(self.geo_sqlcontainer_class(sensor_id=temp_sensor_id, valid_from=valid_from, geom=geom))
                # **************************
                apiparam_containers.append(apiparam_adapter.adapt(packet=packet, sensor_id=temp_sensor_id))
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
