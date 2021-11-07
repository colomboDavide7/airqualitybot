#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 08:30
# @Description: this script contains the classes for initializing the database with different sensor's data.
#
#################################################
import builtins
from abc import ABC, abstractmethod

# IMPORT GLOBAL VARIABLE FROM FETCH MODULE
import airquality.constants.system_constants as sc

# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.parser.datetime_parser import DatetimeParser
from airquality.geom.postgis_geometry import PostGISPoint, PostGISGeometryFactory
from airquality.adapter.geom_adapter import GeometryAdapterPurpleair, GeometryAdapterFactory
from airquality.adapter.container_adapter import ContainerAdapterFactory, ContainerAdapterPurpleair
from airquality.container.sql_container import SensorSQLContainer, GeoSQLContainer, APIParamSQLContainer
from airquality.container.sql_container_factory import SQLContainerFactory
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.api.url_builder import URLBuilderFactory, URLBuilderPurpleair
from airquality.reshaper.api_packet_reshaper import APIPacketReshaperFactory
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.api.urllib_adapter import UrllibAdapter
from airquality.picker.resource_picker import ResourcePicker
from airquality.parser.file_parser import FileParserFactory
from airquality.io.io import IOManager

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, DEBUG_HEADER, INFO_HEADER


class InitializeBot(ABC):

    @abstractmethod
    def run(self):
        pass


class InitializeBotPurpleair(InitializeBot):

    def run(self):

        ################################ READ SERVER FILE ################################
        raw_server_data = IOManager.open_read_close_file(path=SERVER_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=SERVER_FILE.split('.')[-1])
        parsed_server_data = parser.parse(raw_string=raw_server_data)

        ################################ PICK DATABASE CONNECTION PROPERTIES ################################
        db_settings = ResourcePicker.pick_db_conn_properties(parsed_resources=parsed_server_data,
                                                             bot_personality=sc.PERSONALITY)

        ################################ DATABASE CONNECTION ADAPTER ################################
        db_conn_factory = Psycopg2ConnectionAdapterFactory()
        dbconn = db_conn_factory.create_database_connection_adapter(settings=db_settings)
        dbconn.open_conn()

        ################################ SQL QUERY BUILDER ###############################
        raw_query_data = IOManager.open_read_close_file(path=QUERY_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=QUERY_FILE.split('.')[-1])
        parsed_query_data = parser.parse(raw_string=raw_query_data)
        query_builder = SQLQueryBuilder(parsed_query_data)

        ################################ SELECT SENSOR NAME FROM DATABASE ################################
        # The 'sensor_names' variable is used to check if a given sensor taken from the API is already present
        # into the database.
        query = query_builder.select_sensor_name_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensor_names = DatabaseAnswerParser.parse_single_attribute_answer(response=answer)

        if not sensor_names:
            print(f"{INFO_HEADER} no sensor found for personality='{sc.PERSONALITY}'.")
        else:
            if sc.DEBUG_MODE:
                print(20 * "=" + " SENSORS FOUND " + 20 * '=')
                for name in sensor_names:
                    print(f"{DEBUG_HEADER} name='{name}'.")

        ################################ SELECT THE SENSOR ID FOR THE NEXT INSERTIONS ################################
        # Since we have to insert new sensors we need some information:
        #   - the sensor already exist?
        #   - the max sensor id from the sensor table (needed as 'foreign key' for other tables)

        sensor_id = 1
        query = query_builder.select_max_sensor_id()
        answer = dbconn.send(executable_sql_query=query)
        max_sensor_id = DatabaseAnswerParser.parse_single_attribute_answer(answer)
        if max_sensor_id[0] is not None:
            print(f"{INFO_HEADER} max sensor_id found in the database is => {str(max_sensor_id[0])}.")
            sensor_id = max_sensor_id[0] + 1

        ################################ READ API FILE ################################
        raw_api_data = IOManager.open_read_close_file(path=API_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(raw_string=raw_api_data)

        ################################ QUERYSTRING BUILDER ################################
        url_builder_fact = URLBuilderFactory(url_builder_class=URLBuilderPurpleair)
        url_builder = url_builder_fact.create_url_builder()
        url = url_builder.build_url(parameters=parsed_api_data[sc.PERSONALITY])

        ################################ FETCHING API DATA ################################
        raw_api_packets = UrllibAdapter.fetch(url=url)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension='json')
        parsed_api_packets = parser.parse(raw_string=raw_api_packets)

        ################ RESHAPE API DATA FOR GETTING THEM IN A BETTER SHAPE FOR CREATING A CONTAINER ####################
        reshaper = APIPacketReshaperFactory().create_api_packet_reshaper(bot_personality=sc.PERSONALITY)
        reshaped_packets = reshaper.reshape_packet(api_answer=parsed_api_packets)

        if reshaped_packets:
            if sc.DEBUG_MODE:
                print(20 * "=" + " RESHAPED API PACKETS " + 20 * '=')
                for packet in reshaped_packets:
                    print(30 * '*')
                    for key, val in packet.items():
                        print(f"{DEBUG_HEADER} {key}={val}")

            ############################## ADAPTED PACKETS #############################
            # Create a ContainerAdapter object for adapting the packets to the general container interface (dict keys)
            container_adapter_fact = ContainerAdapterFactory(container_adapter_class=ContainerAdapterPurpleair)
            container_adapter = container_adapter_fact.make_container_adapter()

            # Create GeometryContainerAdapter for properly transforming geometry
            geom_adapter_fact = GeometryAdapterFactory(geom_adapter_class=GeometryAdapterPurpleair)
            geom_adapter = geom_adapter_fact.make_geometry_adapter()

            # Create the postgis geometry factory for adapting geometry into
            postgis_geom_fact = PostGISGeometryFactory(geom_class=PostGISPoint)

            # Adapt packets for building container
            adapted_packets = []
            for packet in reshaped_packets:
                geom_adapted_packet = geom_adapter.adapt_packet(packet)
                geometry = postgis_geom_fact.create_geometry(geom_adapted_packet)
                packet['geometry'] = geometry.get_database_string()
                packet['timestamp'] = DatetimeParser.current_sqltimestamp()
                adapted_packet = container_adapter.adapt_packet(packet=packet)
                adapted_packets.append(adapted_packet)

            filtered_packets = []
            for packet in adapted_packets:
                if packet['name'] not in sensor_names:
                    filtered_packets.append(packet)

            if filtered_packets:

                ############################## SENSOR CONTAINERS #############################
                container_factory = SQLContainerFactory(container_class=SensorSQLContainer)
                sensor_containers = container_factory.make_container_with_start_sensor_id(packets=adapted_packets, start_sensor_id=sensor_id)

                # Create a query for inserting sensors
                query_statement = query_builder.insert_into_sensor()
                query = sensor_containers.sql(query=query_statement)
                dbconn.send(executable_sql_query=query)

                ############################## API PARAM CONTAINERS #############################
                container_factory = SQLContainerFactory(container_class=APIParamSQLContainer)
                apiparam_containers = container_factory.make_container_with_start_sensor_id(packets=adapted_packets, start_sensor_id=sensor_id)

                # Create query for inserting api parameters
                query_statement = query_builder.insert_into_api_param()
                query = apiparam_containers.sql(query=query_statement)
                dbconn.send(executable_sql_query=query)

                ############################## SENSOR AT LOCATION CONTAINERS #############################
                container_factory = SQLContainerFactory(container_class=GeoSQLContainer)
                geo_containers = container_factory.make_container_with_start_sensor_id(packets=adapted_packets, start_sensor_id=sensor_id)

                # Create query for inserting sensor at location
                query_statement = query_builder.insert_into_sensor_at_location()
                query = geo_containers.sql(query=query_statement)
                dbconn.send(executable_sql_query=query)
            else:
                print(f"{INFO_HEADER} all sensors are already present into the database.")
        else:
            print(f"{INFO_HEADER} empty packets.")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        dbconn.close_conn()


################################ FACTORY ################################
class InitializeBotFactory(builtins.object):

    @classmethod
    def create_initialize_bot(cls, bot_personality: str) -> InitializeBot:

        if bot_personality == "purpleair":
            return InitializeBotPurpleair()
        else:
            raise SystemExit(f"{InitializeBotFactory.__name__}: cannot instantiate {InitializeBot.__name__} "
                             f"instance for personality='{bot_personality}'.")
