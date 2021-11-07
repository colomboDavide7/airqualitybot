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
from airquality.api.url_builder import URLBuilderFactory
from airquality.parser.file_parser import FileParserFactory
from airquality.parser.datetime_parser import DatetimeParser
from airquality.database.db_conn_adapter import ConnectionAdapter
from airquality.adapter.geom_adapter import GeometryAdapterFactory
from airquality.geom.postgis_geometry import PostGISGeometryFactory
from airquality.reshaper.packet_reshaper import PacketReshaperFactory
from airquality.adapter.container_adapter import ContainerAdapterFactory
from airquality.container.sql_container_factory import SQLContainerFactory

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, INFO_HEADER


################################ INITIALIZE BOT ################################
class InitializeBot:

    def __init__(self,
                 dbconn: ConnectionAdapter,     # database connection adapter object
                 url_builder_class,             # builder class for creating the URL for fetching data from API
                 reshaper_class,                # reshaper class for getting the packets in a better shape
                 container_adapter_class,       # adapter class for all sensor's information
                 geom_adapter_class,            # adapter class for geolocation information
                 postgis_geom_class,            # geometry class for building database geometry string
                 sensor_sqlcontainer_class,     # container class for translating Dict into SQL string
                 apiparam_sqlcontainer_class,   # container class for translating Dict into SQL string
                 geo_sqlcontainer_class):       # container class for translating Dict into SQL string
        self.dbconn = dbconn
        self.url_builder_class = url_builder_class
        self.reshaper_class = reshaper_class
        self.container_adapter_class = container_adapter_class
        self.geom_adapter_class = geom_adapter_class
        self.postgis_geom_class = postgis_geom_class
        self.sensor_sqlcontainer_class = sensor_sqlcontainer_class
        self.apiparam_sqlcontainer_class = apiparam_sqlcontainer_class
        self.geo_sqlcontainer_class = geo_sqlcontainer_class

    def run(self,
            first_sensor_id: int,               # first sensor id from which starts to count
            url_builder_param: Dict[str, Any],  # parameters for building URL for fetching data from API
            sensor_names: List[str],            # list of the name of the sensor present in database or []
            sensor_query: str,                  # INSERT INTO query for inserting records into 'sensor' table
            api_param_query: str,               # INSERT INTO query for inserting records into 'api_param' table
            sensor_at_location_query: str):     # INSERT INTO query for inserting records into 'sensor_at_location' table

        ################################ URL BUILDER ################################
        url_builder_fact = URLBuilderFactory(url_builder_class=self.url_builder_class)
        url_builder = url_builder_fact.create_url_builder()

        ################################ BUILD URL ################################
        url = url_builder.build_url(parameters=url_builder_param)

        ################################ FETCHING API DATA ################################
        raw_api_packets = UrllibAdapter.fetch(url=url)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension='json')
        parsed_api_packets = parser.parse(raw_string=raw_api_packets)

        ################################ RESHAPE PACKETS ################################
        reshaper_fact = PacketReshaperFactory(reshaper_class=self.reshaper_class)
        packet_reshaper = reshaper_fact.make_reshaper()
        reshaped_packets = packet_reshaper.reshape_packet(api_answer=parsed_api_packets)

        if reshaped_packets:
            if sc.DEBUG_MODE:
                print(20 * "=" + " RESHAPED PACKETS " + 20 * '=')
                for packet in reshaped_packets:
                    print(30 * '*')
                    for key, val in packet.items():
                        print(f"{DEBUG_HEADER} {key}={val}")

            ############################## CONTAINER ADAPTER #############################
            container_adapter_fact = ContainerAdapterFactory(container_adapter_class=self.container_adapter_class)
            container_adapter = container_adapter_fact.make_container_adapter()

            ############################## GEOMETRY ADAPTER #############################
            geom_adapter_fact = GeometryAdapterFactory(geom_adapter_class=self.geom_adapter_class)
            geom_adapter = geom_adapter_fact.make_geometry_adapter()

            ############################## POSTGIS ADAPTER #############################
            postgis_geom_fact = PostGISGeometryFactory(geom_class=self.postgis_geom_class)

            ############################## ADAPT PACKETS TO SQL CONTAINER INTERFACE #############################
            adapted_packets = []
            for packet in reshaped_packets:
                geom_adapted_packet = geom_adapter.adapt(packet)
                geometry = postgis_geom_fact.create_geometry(geom_adapted_packet)
                packet['geometry'] = geometry.get_database_string()
                packet['timestamp'] = DatetimeParser.current_sqltimestamp()
                adapted_packet = container_adapter.adapt(packet=packet)
                adapted_packets.append(adapted_packet)

            ############################## FILTER PACKETS BASED ON SENSOR NAME #############################
            filtered_packets = []
            for packet in adapted_packets:
                if packet['name'] not in sensor_names:
                    filtered_packets.append(packet)

            ############################## BUILD SQL CONTAINERS AND EXECUTE QUERIES #############################

            if filtered_packets:
                ############################## SENSOR CONTAINERS #############################
                container_factory = SQLContainerFactory(container_class=self.sensor_sqlcontainer_class)
                sensor_containers = container_factory.make_container_with_start_sensor_id(
                    packets=adapted_packets, start_sensor_id=first_sensor_id
                )

                ############################## API PARAM CONTAINERS #############################
                container_factory = SQLContainerFactory(container_class=self.apiparam_sqlcontainer_class)
                apiparam_containers = container_factory.make_container_with_start_sensor_id(
                    packets=adapted_packets, start_sensor_id=first_sensor_id
                )

                ############################## SENSOR AT LOCATION CONTAINERS #############################
                container_factory = SQLContainerFactory(container_class=self.geo_sqlcontainer_class)
                geo_containers = container_factory.make_container_with_start_sensor_id(
                    packets=adapted_packets, start_sensor_id=first_sensor_id
                )

                ############################## BUILD THE QUERY FROM CONTAINERS #############################
                query = sensor_containers.sql(query=sensor_query)
                query += apiparam_containers.sql(query=api_param_query)
                query += geo_containers.sql(query=sensor_at_location_query)
                self.dbconn.send(executable_sql_query=query)

            else:
                print(f"{INFO_HEADER} all sensors are already present into the database.")
        else:
            print(f"{INFO_HEADER} empty packets.")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
