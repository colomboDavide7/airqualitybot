#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 11:21
# @Description: this script defines the classes for running the geo bot
#
#################################################
import builtins
from abc import ABC, abstractmethod

# IMPORT GLOBAL VARIABLE FROM FETCH MODULE
import airquality.constants.system_constants as sc

# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.adapter.sensor_adapter import SensorAdapterFactory, SensorAdapterPurpleair
from airquality.parser.datetime_parser import DatetimeParser
from airquality.geom.postgis_geometry import PostGISGeometryFactory, PostGISPoint
from airquality.adapter.geom_adapter import GeometryAdapterFactory, GeometryAdapterPurpleair
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


################################ GEO BOT ABSTRACT BASE CLASS ################################
class GeoBot(ABC):

    @abstractmethod
    def run(self):
        pass


class GeoBotPurpleair(GeoBot):

    def run(self):

        ################################ READ SERVER FILE ################################
        raw_server_data = IOManager.open_read_close_file(path=SERVER_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=SERVER_FILE.split('.')[-1])
        parsed_server_data = parser.parse(raw_string=raw_server_data)

        ################################ PICK DATABASE CONNECTION PROPERTIES ################################
        db_settings = ResourcePicker.pick_db_conn_properties(parsed_resources=parsed_server_data,
                                                             bot_personality=sc.PERSONALITY)
        if sc.DEBUG_MODE:
            print(20 * "=" + " DATABASE SETTINGS " + 20 * '=')
            for key, val in db_settings.items():
                print(f"{DEBUG_HEADER} {key}={val}")

        ################################ DATABASE CONNECTION ADAPTER ################################
        db_conn_factory = Psycopg2ConnectionAdapterFactory()
        dbconn = db_conn_factory.create_database_connection_adapter(settings=db_settings)
        dbconn.open_conn()

        ################################ SQL QUERY BUILDER ###############################
        raw_query_data = IOManager.open_read_close_file(path=QUERY_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=QUERY_FILE.split('.')[-1])
        parsed_query_data = parser.parse(raw_string=raw_query_data)
        query_builder = SQLQueryBuilder(parsed_query_data)

        ########### QUERY SENSOR NAME 2 SENSOR ID MAPPING FOR ASSOCIATE AN API PACKET TO A DATABASE RECORD #############
        query = query_builder.select_sensor_name_id_map_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensorname2id_map = DatabaseAnswerParser.parse_key_val_answer(answer)

        if not sensorname2id_map:
            print(f"{INFO_HEADER} no sensor found for personality='{sc.PERSONALITY}'.")
            dbconn.close_conn()
            return

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

        ################ RESHAPE API DATA FOR GETTING THEM IN A BETTER SHAPE FOR DATABASE INSERTION ####################
        reshaper = APIPacketReshaperFactory().create_api_packet_reshaper(bot_personality=sc.PERSONALITY)
        reshaped_packets = reshaper.reshape_packet(api_answer=parsed_api_packets)
        if sc.DEBUG_MODE:
            print(20 * "=" + " RESHAPED API PACKETS " + 20 * '=')
            for packet in reshaped_packets:
                print(30 * '*')
                for key, val in packet.items():
                    print(f"{DEBUG_HEADER} {key}={val}")

        # Create a GeometryAdapter
        geom_adapter_factory = GeometryAdapterFactory(geom_adapter_class=GeometryAdapterPurpleair)
        geom_adapter = geom_adapter_factory.make_geometry_adapter()

        # Create a SensorAdapter
        sensor_adapter_fact = SensorAdapterFactory(sensor_adapter_class=SensorAdapterPurpleair)
        sensor_adapter = sensor_adapter_fact.make_adapter()

        # Create a PostGISGeometryFactory for making the geometry object
        postgis_geom_fact = PostGISGeometryFactory(geom_class=PostGISPoint)

        # Make packets compliant to the interface {'name': 'geom'} to compare them with the old locations packet pulled down
        # from the database.
        new_locations = {}
        for packet in reshaped_packets:
            sensor_adapted_packet = sensor_adapter.adapt_packet(packet)
            geom_adapted_packet = geom_adapter.adapt_packet(packet)
            geometry = postgis_geom_fact.create_geometry(geom_adapted_packet)
            new_locations[sensor_adapted_packet['name']] = geometry.get_geomtype_string()

        # Now the packets are in the form {'name': 'geom'} like those pulled down from the database

        ########################## QUERY THE ACTIVE LOCATION FOR PURPLEAIR STATIONS ################################
        query = query_builder.select_sensor_valid_geo_map_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensorid2geom_map = DatabaseAnswerParser.parse_key_val_answer(answer)

        # Create the active locations
        active_locations = {}
        for name in sensorname2id_map.keys():
            sensor_id = sensorname2id_map[name]
            if sensor_id in sensorid2geom_map.keys():
                active_locations[name] = sensorid2geom_map[sensor_id]

        if sc.DEBUG_MODE:
            if active_locations:
                print(20 * "=" + " ACTIVE LOCATIONS " + 20 * '=')
                for key, val in active_locations.items():
                    print(f"{DEBUG_HEADER} {key}={val}")

        ############## COMPARE THE OLD LOCATIONS WITH THE NEW DOWNLOADED FROM THE API ###################

        # CYCLE THROUGH THE RESHAPED API PACKETS (SENSOR_ID: GEOM)
        for name in new_locations.keys():
            if name in active_locations.keys():
                # compare the locations
                if new_locations[name] != active_locations[name]:

                    # update the old location 'valid_to' timestamp
                    ts = DatetimeParser.current_sqltimestamp()
                    query = query_builder.update_valid_to_timestamp_location(timestamp=ts, sensor_id=sensorname2id_map[name])
                    dbconn.send(executable_sql_query=query)

                    # insert new record corresponding to the sensor_id with the
                    query_statement = query_builder.insert_into_sensor_at_location()
                    query_statement += f"({sensorname2id_map[name]}, '{ts}', ST_GeomFromText('{new_locations[name]}', 26918));"
                    dbconn.send(executable_sql_query=query_statement)

                else:
                    print(f"{INFO_HEADER} old_location='{active_locations[name]}' is equal to new_location='{new_locations[name]}'")
            else:
                print(f"{INFO_HEADER} name='{name}' is not an active locations...")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        dbconn.close_conn()


################################ FACTORY ################################
class GeoBotFactory(builtins.object):

    @classmethod
    def create_geo_bot(cls, bot_personality: str) -> GeoBot:

        if bot_personality == "purpleair":
            return GeoBotPurpleair()
        else:
            raise SystemExit(f"{GeoBotFactory.__name__}: cannot instantiate {GeoBot.__name__} "
                             f"instance for personality='{bot_personality}'.")
