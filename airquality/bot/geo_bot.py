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
from airquality.packet.geoparam_packet import GeoParamPacketPurpleair
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.api.url_querystring_builder import URLQuerystringBuilderFactory
from airquality.reshaper.api_packet_reshaper import APIPacketReshaperFactory
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.keeper.api_packet_keeper import APIPacketKeeperFactory
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.picker.json_param_picker import JSONParamPicker
from airquality.picker.resource_picker import ResourcePicker
from airquality.parser.file_parser import FileParserFactory
from airquality.io.io import IOManager

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, DEBUG_HEADER, EMPTY_LIST


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

        ################################ SQL QUERY BUILDER ################################
        query_builder = SQLQueryBuilder(query_file_path=QUERY_FILE)

        ################ SELECT SENSOR IDS FROM PERSONALITY (same method used for selecting sensor names) ###############
        query = query_builder.select_sensor_ids_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensor_ids = DatabaseAnswerParser.parse_single_attribute_answer(response=answer)

        ################################ IF THERE ARE NO SENSORS, THE PROGRAM STOPS HERE ###############################
        if sensor_ids == EMPTY_LIST:
            if sc.DEBUG_MODE:
                print(f"{DEBUG_HEADER} no sensor associated to personality = '{sc.PERSONALITY}'.")
            dbconn.close_conn()
            return

        ################################ SELECT SENSOR NAME FROM DATABASE ################################
        # The 'sensor_names' variable is used to check if a given sensor taken from the API is already present
        # into the database.
        query = query_builder.select_sensor_name_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensor_names = DatabaseAnswerParser.parse_single_attribute_answer(response=answer)

        if sc.DEBUG_MODE:
            if sensor_names != EMPTY_LIST:
                for name in sensor_names:
                    print(f"{DEBUG_HEADER} name = '{name}' is already present.")
            else:
                print(f"{DEBUG_HEADER} no sensor found for personality '{sc.PERSONALITY}'.")

        ################################ READ API FILE ################################
        raw_api_data = IOManager.open_read_close_file(path=API_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(raw_string=raw_api_data)

        ################################ PICK API ADDRESS FROM PARSED JSON DATA ################################
        path2key = [sc.PERSONALITY, "api_address"]
        api_address = JSONParamPicker.pick_parameter(parsed_json=parsed_api_data, path2key=path2key)
        if sc.DEBUG_MODE:
            print(20 * "=" + " API ADDRESS " + 20 * '=')
            print(f"{DEBUG_HEADER} {api_address}")

        ################################ API REQUEST ADAPTER ################################
        api_adapter = APIRequestAdapter(api_address=api_address)

        ################################ QUERYSTRING BUILDER ################################
        querystring_builder = URLQuerystringBuilderFactory.create_querystring_builder(bot_personality=sc.PERSONALITY)
        querystring = querystring_builder.make_querystring(parameters=parsed_api_data[sc.PERSONALITY])

        ################################ FETCHING API DATA ################################
        raw_api_packets = api_adapter.fetch(querystring=querystring)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension='json')
        parsed_api_packets = parser.parse(raw_string=raw_api_packets)

        ################ RESHAPE API DATA FOR GETTING THEM IN A BETTER SHAPE FOR DATABASE INSERTION ####################
        reshaper = APIPacketReshaperFactory().create_api_packet_reshaper(bot_personality=sc.PERSONALITY)
        reshaped_packets = reshaper.reshape_packet(api_answer=parsed_api_packets)
        if sc.DEBUG_MODE:
            print(20 * "=" + " RESHAPED API PACKETS " + 20 * '=')
            for packet in reshaped_packets:
                print(30 * '*')
                print(f"{DEBUG_HEADER} {str(packet)}")

        ####### CREATE PACKET KEEPER FOR KEEPING ONLY THOSE PACKETS FROM SENSORS ALREADY PRESENT INTO THE DATABASE ########
        keeper = APIPacketKeeperFactory().create_packet_keeper(bot_personality=sc.PERSONALITY)
        filtered_packets = keeper.keep_packets(packets=reshaped_packets, identifiers=sensor_names)

        if sc.DEBUG_MODE:
            print(20 * "=" + " FILTERED PACKETS " + 20 * '=')
            for packet in filtered_packets:
                print(30 * '*')
                print(f"{DEBUG_HEADER} {str(packet)}")

        ########### QUERY SENSOR NAME 2 SENSOR ID MAPPING FOR ASSOCIATE AN API PACKET TO A DATABASE RECORD #############
        query = query_builder.select_sensor_name_id_map_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensorname2id_map = DatabaseAnswerParser.parse_key_val_answer(answer)

        ########################## QUERY THE ACTIVE LOCATION FOR PURPLEAIR STATIONS ################################
        query = query_builder.select_sensor_valid_geo_map_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensorid2geom_map = DatabaseAnswerParser.parse_key_val_answer(answer)

        if sc.DEBUG_MODE:
            if sensorid2geom_map != EMPTY_LIST:
                print(20 * "=" + " ACTIVE LOCATIONS " + 20 * '=')
                for key, val in sensorid2geom_map.items():
                    print(f"{DEBUG_HEADER} {key}={val}")

        ############## CREATE GEO PARAM PACKETS BY ASSOCIATING THE ID TO THE SENSOR_IDENTIFIER ########################
        # These packets are used ONLY in case of insertion (new position detected) !!!
        geo_param_packets = []
        for packet in filtered_packets:
            sensor_id = sensorname2id_map[packet.purpleair_identifier]
            geo_param_packets.append(GeoParamPacketPurpleair(packet=packet, sensor_id=sensor_id))

        if sc.DEBUG_MODE:
            if sensorid2geom_map != EMPTY_LIST:
                print(20 * "=" + " GEO PARAM PACKETS " + 20 * '=')
                for packet in geo_param_packets:
                    print(30 * '*')
                    print(f"{DEBUG_HEADER} {str(packet)}")

        ############## COMPARE THE OLD LOCATIONS WITH THE NEW DOWNLOADED FROM THE API ###################

        # CYCLE THROUGH THE RESHAPED API PACKETS (SENSOR_ID: GEOM)
        for packet in geo_param_packets:

            old_location = sensorid2geom_map.get(packet.sensor_id)
            new_location = packet.point.get_geomtype_string()

            if new_location != old_location:

                # update the old location 'valid_to' timestamp
                query = query_builder.update_valid_to_timestamp_location(sensor_id=packet.sensor_id)
                dbconn.send(executable_sql_query=query)

                # insert new record corresponding to the geo param packet
                query = query_builder.insert_single_sensor_at_location(packet=packet)
                dbconn.send(executable_sql_query=query)


################################ FACTORY ################################
class GeoBotFactory(builtins.object):

    @classmethod
    def create_geo_bot(cls, bot_personality: str) -> GeoBot:

        if bot_personality == "purpleair":
            return GeoBotPurpleair()
        else:
            raise SystemExit(f"{GeoBotFactory.__name__}: cannot instantiate {GeoBot.__name__} "
                             f"instance for personality='{bot_personality}'.")
