#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 11:33
# @Description: this script defines the bot classes for the fetch module
#
#################################################
import builtins
from abc import ABC, abstractmethod

# IMPORT GLOBAL VARIABLE FROM FETCH MODULE
import airquality.constants.system_constants as sc

# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.reshaper.api2db_station_reshaper import API2DatabaseStationReshaperFactory
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.filter.datetime_packet_filter import DatetimePacketFilterFactory
from airquality.api.url_querystring_builder import URLQuerystringBuilderFactory
from airquality.reshaper.api_packet_reshaper import APIPacketReshaperFactory
from airquality.reshaper.api2db_reshaper import API2DatabaseReshaperFactory
from airquality.reshaper.db2api_reshaper import Database2APIReshaperFactory
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.parser.datetime_parser import DatetimeParser
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.picker.json_param_picker import JSONParamPicker
from airquality.picker.resource_picker import ResourcePicker
from airquality.parser.file_parser import FileParserFactory
from airquality.io.io import IOManager

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, DEBUG_HEADER, \
    EMPTY_LIST, PURPLEAIR_PERSONALITY


################################################################################################


class FetchBot(ABC):


    @abstractmethod
    def run(self):
        pass





class FetchBotThingspeak(FetchBot):


    def run(self):

        ################################ READ SERVER FILE ################################
        raw_server_data = IOManager.open_read_close_file(path = SERVER_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = SERVER_FILE.split('.')[-1])
        parsed_server_data = parser.parse(raw_string = raw_server_data)

        ################################ PICK DATABASE CONNECTION PROPERTIES ################################
        db_settings = ResourcePicker.pick_db_conn_properties(parsed_resources = parsed_server_data,
                                                             bot_personality = sc.PERSONALITY)
        if sc.DEBUG_MODE:
            print(20 * "=" + " DATABASE SETTINGS " + 20 * '=')
            for key, val in db_settings.items():
                print(f"{DEBUG_HEADER} {key}={val}")

        ################################ DATABASE CONNECTION ADAPTER ################################
        db_conn_factory = Psycopg2ConnectionAdapterFactory()
        dbconn = db_conn_factory.create_database_connection_adapter(settings = db_settings)
        dbconn.open_conn()

        ################################ SQL QUERY BUILDER ################################
        query_builder = SQLQueryBuilder(query_file_path = QUERY_FILE)

        ################################ READ API FILE ################################
        raw_setup_data = IOManager.open_read_close_file(path = API_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(raw_string = raw_setup_data)

        ################################ PICK API ADDRESS FROM PARSED JSON DATA ################################
        path2key = [sc.PERSONALITY, "api_address", sc.API_ADDRESS_N]
        api_address = JSONParamPicker.pick_parameter(parsed_json = parsed_api_data, path2key = path2key)
        if sc.DEBUG_MODE:
            print(20 * "=" + " API ADDRESS " + 20 * '=')
            print(f"{DEBUG_HEADER} {api_address}")

        ################################ QUERYSTRING BUILDER ################################
        querystring_builder = URLQuerystringBuilderFactory().create_querystring_builder(bot_personality = sc.PERSONALITY)


        ################################ SELECT SENSOR IDS FROM IDENTIFIER ################################
        query = query_builder.select_sensor_ids_from_identifier(identifier = PURPLEAIR_PERSONALITY)
        answer = dbconn.send(executable_sql_query = query)
        sensor_ids = DatabaseAnswerParser.parse_single_attribute_answer(response = answer)

        if sc.DEBUG_MODE:
            print(20 * "=" + " DATABASE SENSOR IDS " + 20 * '=')
            for id_ in sensor_ids:
                print(f"{DEBUG_HEADER} {id_}")

################################ IF THERE ARE NO SENSORS, THE PROGRAM STOPS HERE ################################
        if sensor_ids == EMPTY_LIST:
            if sc.DEBUG_MODE:
                print(f"{DEBUG_HEADER} no sensor associated to personality = '{PURPLEAIR_PERSONALITY}'.")
            dbconn.close_conn()
            return

        ################################ SELECT MEASURE PARAM FROM IDENTIFIER ################################
        query = query_builder.select_measure_param_from_identifier(identifier = PURPLEAIR_PERSONALITY)
        answer = dbconn.send(executable_sql_query = query)
        measure_param_map = DatabaseAnswerParser.parse_key_val_answer(answer)

        if sc.DEBUG_MODE:
            print(20 * "=" + " MEASURE PARAM MAPPING " + 20 * '=')
            for code, id_ in measure_param_map.items():
                print(f"{DEBUG_HEADER} {code}={id_}")

################################ FOR EACH SENSOR DO THE STUFF BELOW ################################

        for sensor_id in sensor_ids:

            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ###################### SELECT LAST SENSOR MEASUREMENT TIMESTAMP FROM DATABASE ##############################
            query = query_builder.select_last_acquisition_timestamp_from_station_id(station_id = sensor_id)
            answer = dbconn.send(executable_sql_query = query)
            parsed_timestamp = DatabaseAnswerParser.parse_single_attribute_answer(answer)

            if sc.DEBUG_MODE:
                if parsed_timestamp == EMPTY_LIST:
                    print(f"{DEBUG_HEADER} no measure present into the database for sensor_id = {sensor_id}.")
                else:
                    print(f"{DEBUG_HEADER} {parsed_timestamp[0]}")


            ################################ SELECT SENSOR API PARAM FROM DATABASE ################################
            query = query_builder.select_sensor_api_param(sensor_id = sensor_id)
            answer = dbconn.send(executable_sql_query = query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            if sc.DEBUG_MODE:
                print(20 * "=" + " API PARAMETERS " + 20 * '=')
                for name, value in api_param.items():
                    print(f"{DEBUG_HEADER} {name}={value}")

            ################### RESHAPE API DATA FOR GETTING THE COUPLE CHANNEL_ID: CHANNEL_KEY ########################
            db2api_reshaper = Database2APIReshaperFactory().create_reshaper(bot_personality = sc.PERSONALITY)
            reshaped_api_param = db2api_reshaper.reshape_data(api_param = api_param)

            if sc.DEBUG_MODE:
                print(20 * "=" + " RESHAPED API PARAM " + 20 * '=')
                for ch_id, ch_key in reshaped_api_param.items():
                    print(f"{DEBUG_HEADER} {ch_id}={ch_key}")


################################ FORMAT API ADDRESS AND BUILD QUERYSTRING FOR EACH CHANNEL ################################

            for channel_id in reshaped_api_param.keys():

                # FORMAT API ADDRESS WITH CHANNEL ID
                formatted_api_address = api_address.format(channel_id = channel_id)

                # CREATE API REQUEST ADAPTER
                api_adapter = APIRequestAdapter(api_address = formatted_api_address)
                if sc.DEBUG_MODE:
                    print(20 * "=" + " API ADDRESS " + 20 * '=')
                    print(f"{DEBUG_HEADER} {formatted_api_address}")

################################ DEFINE START DATE AND STOP DATE FOR FETCHING DATA FROM API ################################

                stop_date = DatetimeParser.today()
                from_date = DatetimeParser.string2date(date = '2018-01-01 00:00:00')

                # CHECK IF THERE ARE MEASUREMENTS ALREADY PRESENT INTO THE DATABASE FOR THE GIVEN SENSOR_ID
                if parsed_timestamp != EMPTY_LIST:
                    # CHECK IF THERE ARE SOME MEASUREMENTS TO FETCH
                    if (parsed_timestamp[0] - stop_date).total_seconds() < 0:
                        from_date = parsed_timestamp[0]

                to_date   = DatetimeParser.add_days_to_date(date = from_date, days = 7)
                if (to_date - stop_date).total_seconds() > 0:
                    to_date = stop_date

                # CONTINUE UNTIL TODAY IS REACHED
                while (stop_date - from_date).total_seconds() >= 0:

                    # GET QUERYSTRING PARAMETERS
                    querystring_param = {'api_key': reshaped_api_param[channel_id],
                                         'start': DatetimeParser.date2string(date = from_date),
                                         'end': DatetimeParser.date2string(date = to_date)}

                    # BUILD URL QUERYSTRING
                    querystring = querystring_builder.make_querystring(parameters = querystring_param)
                    if sc.DEBUG_MODE:
                        print(20 * "=" + " URL QUERYSTRING " + 20 * '=')
                        print(f"{DEBUG_HEADER} {querystring}")


                    # FETCH DATA FROM API
                    api_packets = api_adapter.fetch(querystring)
                    parser = FileParserFactory.file_parser_from_file_extension(file_extension = "json")
                    parsed_api_packets = parser.parse(raw_string = api_packets)

                    # if sc.DEBUG_MODE:
                    #     print(20 * "=" + " API PACKETS " + 20 * '=')
                    #     if parsed_api_packets["feeds"] != EMPTY_LIST:
                    #         for i in range(3):
                    #             packet = parsed_api_packets["feeds"][i]
                    #             for key, val in packet.items():
                    #                 print(f"{DEBUG_HEADER} {key}={val}")

################################ CONTINUE ONLY IF THERE ARE VALID PACKETS FROM APIS ################################
                    if parsed_api_packets["feeds"] != EMPTY_LIST:

                        ######### API PACKET RESHAPER FOR GETTING THE RIGHT MAPPING FOR NEXT INSERTION #################
                        api_packet_reshaper = APIPacketReshaperFactory().create_api_packet_reshaper(bot_personality = sc.PERSONALITY)
                        reshaped_api_packets = api_packet_reshaper.reshape_packet(api_answer = parsed_api_packets)

                        # if sc.DEBUG_MODE:
                        #     if reshaped_api_packets != EMPTY_LIST:
                        #         print(20 * "=" + " RESHAPED API PACKETS " + 20 * '=')
                        #         for i in range(3):
                        #             packet = reshaped_api_packets[i]
                        #             for key, val in packet.items():
                        #                 print(f"{DEBUG_HEADER} {key}={val}")

                        ############### API 2 DATABASE RESHAPER FOR BUILDING THE QUERY LATER ###########################
                        api2db_reshaper = API2DatabaseStationReshaperFactory().create_reshaper(bot_personality = sc.PERSONALITY)
                        db_ready_packets = api2db_reshaper.reshape_packets(packets = reshaped_api_packets,
                                                                           measure_param_map = measure_param_map,
                                                                           sensor_id = sensor_id)

                        # if sc.DEBUG_MODE:
                        #     if db_ready_packets != EMPTY_LIST:
                        #         print(20 * "=" + " DATABASE READY PACKETS " + 20 * '=')
                        #         for i in range(3):
                        #             packet = db_ready_packets[i]
                        #             for key, val in packet.items():
                        #                 print(f"{DEBUG_HEADER} {key}={val}")

                        ################# BUILD THE QUERY FOR INSERTING THE PACKETS INTO THE DATABASE ##################
                        query = query_builder.insert_station_measurements(packets = db_ready_packets)
                        dbconn.send(executable_sql_query = query)

                        # if sc.DEBUG_MODE:
                        #     print(20 * "=" + " INSERT INTO QUERY " + 20 * '=')
                        #     print(f"{DEBUG_HEADER} {query}")



################################ INCREMENT THE PERIOD FOR DATA FETCHING ################################
                    from_date = DatetimeParser.add_days_to_date(date = from_date, days = 7)
                    to_date = DatetimeParser.add_days_to_date(date = from_date, days = 7)

                    if (to_date - stop_date).total_seconds() >= 0:
                        to_date = stop_date




                    # ################################ FILTER PACKETS FROM LAST TIMESTAMP ON ################################
                    # filter_sqltimestamp = ResourcePicker.pick_last_timestamp_from_api_param_by_personality(
                    #     api_param = api_param,
                    #     personality = PERSONALITY)
                    # filter_ = DatetimePacketFilterFactory().create_datetime_filter(bot_personality = PERSONALITY)
                    # filtered_packets = filter_.filter_packets(packets = api_answer, sqltimestamp = filter_sqltimestamp)
                    #
                    # if DEBUG_MODE:
                    #     print(20 * "=" + " FILTERED PACKETS " + 20 * '=')
                    #     if filtered_packets != EMPTY_LIST:
                    #         for i in range(10):
                    #             rpacket = filtered_packets[i]
                    #             for key, val in rpacket.items():
                    #                 print(f"{DEBUG_HEADER} {key}={val}")


        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        dbconn.close_conn()




################################################################################################


#                                ATMOTUBE BOT FOR FETCHING DATA


################################################################################################

class FetchBotAtmotube(FetchBot):



    def run(self):

        ################################ READ SERVER FILE ################################
        raw_server_data = IOManager.open_read_close_file(path = SERVER_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = SERVER_FILE.split('.')[-1])
        parsed_server_data = parser.parse(raw_string = raw_server_data)

        ################################ PICK DATABASE CONNECTION PROPERTIES ################################
        db_settings = ResourcePicker.pick_db_conn_properties(parsed_resources = parsed_server_data,
                                                             bot_personality = sc.PERSONALITY)
        if sc.DEBUG_MODE:
            print(20 * "=" + " DATABASE SETTINGS " + 20 * '=')
            for key, val in db_settings.items():
                print(f"{DEBUG_HEADER} {key}={val}")

        ################################ DATABASE CONNECTION ADAPTER ################################
        db_conn_factory = Psycopg2ConnectionAdapterFactory()
        dbconn = db_conn_factory.create_database_connection_adapter(settings = db_settings)
        dbconn.open_conn()

        ################################ SQL QUERY BUILDER ################################
        query_builder = SQLQueryBuilder(query_file_path = QUERY_FILE)

        ################################ READ API FILE ################################
        raw_setup_data = IOManager.open_read_close_file(path = API_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(raw_string = raw_setup_data)

        ################################ PICK API ADDRESS FROM PARSED JSON DATA ################################
        path2key = [sc.PERSONALITY, "api_address", sc.API_ADDRESS_N]
        api_address = JSONParamPicker.pick_parameter(parsed_json = parsed_api_data, path2key = path2key)
        if sc.DEBUG_MODE:
            print(20 * "=" + " API ADDRESS " + 20 * '=')
            print(f"{DEBUG_HEADER} {api_address}")

        ################################ API REQUEST ADAPTER ################################
        api_adapter = APIRequestAdapter(api_address = api_address)


        ################################ SELECT SENSOR IDS FROM IDENTIFIER ################################
        query = query_builder.select_sensor_ids_from_identifier(identifier = sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query = query)
        sensor_ids = DatabaseAnswerParser.parse_single_attribute_answer(response = answer)

        if sc.DEBUG_MODE:
            print(20 * "=" + " DATABASE SENSOR IDS " + 20 * '=')
            for id_ in sensor_ids:
                print(f"{DEBUG_HEADER} {id_}")

        ################################ IF THERE ARE NO SENSORS, THE PROGRAM STOPS HERE ################################
        if sensor_ids == EMPTY_LIST:
            if sc.DEBUG_MODE:
                print(f"{DEBUG_HEADER} no sensor associated to personality = '{sc.PERSONALITY}'.")
            dbconn.close_conn()
            return

        ################################ SELECT MEASURE PARAM FROM IDENTIFIER ################################
        query = query_builder.select_measure_param_from_identifier(identifier = sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query = query)
        measure_param_map = DatabaseAnswerParser.parse_key_val_answer(answer)

        if sc.DEBUG_MODE:
            print(20 * "=" + " MEASURE PARAM MAPPING " + 20 * '=')
            for code, id_ in measure_param_map.items():
                print(f"{DEBUG_HEADER} {code}={id_}")

        ################################ FOR EACH SENSOR DO THE STUFF BELOW ################################

        for sensor_id in sensor_ids:

            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT SENSOR API PARAM FROM DATABASE ################################
            query = query_builder.select_sensor_api_param(sensor_id = sensor_id)
            answer = dbconn.send(executable_sql_query = query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            if sc.DEBUG_MODE:
                print(20 * "=" + " API PARAMETERS " + 20 * '=')
                for name, value in api_param.items():
                    print(f"{DEBUG_HEADER} {name}={value}")

            ################################ BUILD URL QUERYSTRING FROM API PARAM ################################
            querystring_builder = URLQuerystringBuilderFactory.create_querystring_builder(bot_personality = sc.PERSONALITY)
            querystring = querystring_builder.make_querystring(parameters = api_param)

            if sc.DEBUG_MODE:
                print(20 * "=" + " URL QUERYSTRING " + 20 * '=')
                print(f"{DEBUG_HEADER} {querystring}")

            ################################ FETCH DATA FROM API ################################
            api_answer = api_adapter.fetch(querystring = querystring)
            parser = FileParserFactory.file_parser_from_file_extension(file_extension = "json")
            api_answer = parser.parse(raw_string = api_answer)

            ################################ FILTER PACKETS FROM LAST TIMESTAMP ON ################################
            filter_sqltimestamp = ResourcePicker.pick_last_timestamp_from_api_param_by_personality(api_param = api_param,
                                                                                                   personality = sc.PERSONALITY)
            filter_ = DatetimePacketFilterFactory().create_datetime_filter(bot_personality = sc.PERSONALITY)
            filtered_packets = filter_.filter_packets(packets = api_answer, sqltimestamp = filter_sqltimestamp)

            if sc.DEBUG_MODE:
                print(20 * "=" + " FILTERED PACKETS " + 20 * '=')
                if filtered_packets != EMPTY_LIST:
                    for i in range(10):
                        rpacket = filtered_packets[i]
                        for key, val in rpacket.items():
                            print(f"{DEBUG_HEADER} {key}={val}")

            ################################ INSERT MEASURE ONLY IF THERE ARE NEW MEASUREMENTS ################################
            if filtered_packets != EMPTY_LIST:

                ################################ RESHAPE API PACKET FOR INSERT MEASURE IN DATABASE #####################
                reshaper = API2DatabaseReshaperFactory().create_api2database_reshaper(bot_personality = sc.PERSONALITY)
                reshaped_packets = reshaper.reshape_packets(packets = filtered_packets,
                                                            measure_param_map = measure_param_map)

                if sc.DEBUG_MODE:
                    print(20 * "=" + " RESHAPED PACKETS " + 20 * '=')
                    if reshaped_packets != EMPTY_LIST:
                        for i in range(10):
                            rpacket = reshaped_packets[i]
                            for key, val in rpacket.items():
                                print(f"{DEBUG_HEADER} {key}={val}")


                ################################ CREATE QUERY FOR INSERTING SENSOR MEASURE TO DATABASE #################
                query = query_builder.insert_atmotube_measurements(reshaped_packets)
                dbconn.send(executable_sql_query = query)


                ############### UPDATE LAST MEASURE TIMESTAMP FOR KNOWING WHERE TO START WITH NEXT FETCH ###############
                if sc.DEBUG_MODE:
                    print(f"{DEBUG_HEADER} last timestamp = {reshaped_packets[-1]['ts']}")

                query = query_builder.update_last_packet_date_atmotube(last_timestamp = reshaped_packets[-1]["ts"],
                                                                       sensor_id = sensor_id)
                dbconn.send(executable_sql_query = query)


        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        dbconn.close_conn()


################################ FACTORY ################################
class FetchBotFactory(builtins.object):

    @classmethod
    def create_fetch_bot(cls, bot_personality: str) -> FetchBot:

        if bot_personality == "thingspeak":
            return FetchBotThingspeak()
        elif bot_personality == "atmotube":
            return FetchBotAtmotube()
        else:
            raise SystemExit(f"{FetchBotFactory.__name__}: cannot instantiate {FetchBot.__name__} "
                             f"instance for personality='{bot_personality}'.")
