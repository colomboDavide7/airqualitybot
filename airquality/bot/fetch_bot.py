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
from airquality.picker.api_param_picker import APIParamPicker
from airquality.picker.resource_picker import ResourcePicker
from airquality.parser.file_parser import FileParserFactory
from airquality.io.io import IOManager

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, DEBUG_HEADER, \
    EMPTY_LIST, PURPLEAIR_PERSONALITY, ATMOTUBE_START_FETCH_TIMESTAMP, THINGSPEAK_START_FETCH_TIMESTAMP


################################################################################################


class FetchBot(ABC):


    @abstractmethod
    def run(self):
        pass



################################################################################################


#                                THINGSPEAK BOT FOR FETCHING DATA


################################################################################################

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
        path2key = [sc.PERSONALITY, "api_address"]
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

        ################################ IF THERE ARE NO SENSORS, THE PROGRAM STOPS HERE ################################
        if sensor_ids == EMPTY_LIST:
            if sc.DEBUG_MODE:
                print(f"{DEBUG_HEADER} no sensor associated to personality = '{PURPLEAIR_PERSONALITY}'.")
            dbconn.close_conn()
            return

        if sc.DEBUG_MODE:
            print(20 * "=" + " DATABASE SENSOR IDS " + 20 * '=')
            for sensor_id in sensor_ids:
                print(f"{DEBUG_HEADER} {sensor_id}")

        ################################ SELECT MEASURE PARAM FROM IDENTIFIER ################################
        query = query_builder.select_measure_param_from_identifier(identifier = PURPLEAIR_PERSONALITY)
        answer = dbconn.send(executable_sql_query = query)
        measure_param_map = DatabaseAnswerParser.parse_key_val_answer(answer)

        if sc.DEBUG_MODE:
            print(20 * "=" + " MEASURE PARAM MAPPING " + 20 * '=')
            for param_code, param_id in measure_param_map.items():
                print(f"{DEBUG_HEADER} {param_code}={param_id}")

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

                stop_datetime = DatetimeParser.today()
                from_datetime = DatetimeParser.string2datetime(datetime_string = THINGSPEAK_START_FETCH_TIMESTAMP)

                # CHECK IF THERE ARE MEASUREMENTS ALREADY PRESENT INTO THE DATABASE FOR THE GIVEN SENSOR_ID
                if parsed_timestamp != EMPTY_LIST:
                    from_datetime = parsed_timestamp[0]

                to_datetime = DatetimeParser.add_days_to_datetime(ts = from_datetime, days = 7)
                if (to_datetime - stop_datetime).total_seconds() > 0:
                    to_datetime = stop_datetime

                # CONTINUE UNTIL TODAY IS REACHED
                while (stop_datetime - from_datetime).total_seconds() >= 0:

                    # GET QUERYSTRING PARAMETERS
                    querystring_param = {'api_key': reshaped_api_param[channel_id],
                                         'start': DatetimeParser.datetime2string(ts = from_datetime),
                                         'end': DatetimeParser.datetime2string(ts = to_datetime)}

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

                        if sc.DEBUG_MODE:
                            if db_ready_packets != EMPTY_LIST:
                                print(20 * "=" + " DATABASE READY PACKETS " + 20 * '=')
                                for packet in db_ready_packets[0:3]:
                                    for key, val in packet.items():
                                        print(f"{DEBUG_HEADER} {key}={val}")

                                for packet in db_ready_packets[-4:-1]:
                                    for key, val in packet.items():
                                        print(f"{DEBUG_HEADER} {key}={val}")

                        ################# BUILD THE QUERY FOR INSERTING THE PACKETS INTO THE DATABASE ##################
                        query = query_builder.insert_station_measurements(packets = db_ready_packets)
                        dbconn.send(executable_sql_query = query)


################################ INCREMENT THE PERIOD FOR DATA FETCHING ################################
                    from_datetime = DatetimeParser.add_days_to_datetime(ts = from_datetime, days = 7)
                    to_datetime = DatetimeParser.add_days_to_datetime(ts = from_datetime, days = 7)

                    if (to_datetime - stop_datetime).total_seconds() >= 0:
                        to_datetime = stop_datetime


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
        raw_api_data = IOManager.open_read_close_file(path = API_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(raw_string = raw_api_data)

        ################################ PICK API ADDRESS FROM PARSED JSON DATA ################################
        path2key = [sc.PERSONALITY, "api_address"]
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

        ################################ IF THERE ARE NO SENSORS, THE PROGRAM STOPS HERE ################################
        if sensor_ids == EMPTY_LIST:
            if sc.DEBUG_MODE:
                print(f"{DEBUG_HEADER} no sensor associated to personality = '{PURPLEAIR_PERSONALITY}'.")
            dbconn.close_conn()
            return

        if sc.DEBUG_MODE:
            print(20 * "=" + " DATABASE SENSOR IDS " + 20 * '=')
            for sensor_id in sensor_ids:
                print(f"{DEBUG_HEADER} {sensor_id}")

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

            ############### ADD OPTIONAL QUERYSTRING PARAMETER READ FROM API FILE ###################
            api_param2pick = ResourcePicker.pick_optional_api_parameters_from_api_data(personality = sc.PERSONALITY)
            optional_params = APIParamPicker.pick_param(api_param = parsed_api_data[sc.PERSONALITY],
                                                        param2pick = api_param2pick)

            if sc.DEBUG_MODE:
                print(20 * "=" + " OPTIONAL API PARAMETERS " + 20 * '=')
                for key, val in optional_params.items():
                    print(f"{DEBUG_HEADER} {key}={val}")

            ################################ MERGE API PARAM WITH OPTIONAL API PARAM ################################
            api_param.update(optional_params)
            if sc.DEBUG_MODE:
                print(20 * "=" + " TOTAL API PARAMETERS " + 20 * '=')
                for name, value in api_param.items():
                    print(f"{DEBUG_HEADER} {name}={value}")

            ################################ CREATE URL QUERYSTRING BUILDER ################################
            querystring_builder = URLQuerystringBuilderFactory.create_querystring_builder(bot_personality = sc.PERSONALITY)

            ################################ CYCLE THROUGH DATE UNTIL NOW ################################
            stop_datetime = DatetimeParser.today()
            from_datetime = DatetimeParser.string2datetime(datetime_string = ATMOTUBE_START_FETCH_TIMESTAMP)

            # IF DATE IS PRESENT INTO THE DATABASE THEN START TO FETCH DATA FROM THAT DATE
            filter_sqltimestamp = ""
            if api_param.get('date', None) is not None:
                from_datetime = DatetimeParser.string2datetime(datetime_string = api_param['date'])
                filter_sqltimestamp = api_param['date']

            while (from_datetime - stop_datetime).total_seconds() < 0:

                # INSERT DATETIME INTO API PARAMETERS
                api_param['date'] = DatetimeParser.datetime2string(ts = from_datetime)

                # BUILD THE QUERYSTRING
                querystring = querystring_builder.make_querystring(parameters = api_param)

                if sc.DEBUG_MODE:
                    print(20 * "=" + " URL QUERYSTRING " + 20 * '=')
                    print(f"{DEBUG_HEADER} {querystring}")

                ################################ FETCH DATA FROM API ################################
                api_answer = api_adapter.fetch(querystring = querystring)
                parser = FileParserFactory.file_parser_from_file_extension(file_extension = "json")
                api_answer = parser.parse(raw_string = api_answer)

                ################# FILTER PACKETS ONLY IF IT IS NOT THE FIRST ACQUISITION FOR THE SENSOR ################
                filter_ = DatetimePacketFilterFactory().create_datetime_filter(bot_personality = sc.PERSONALITY)
                filtered_packets = filter_.filter_packets(packets = api_answer, sqltimestamp = filter_sqltimestamp)

                if sc.DEBUG_MODE:
                    print(20 * "=" + " FILTERED PACKETS " + 20 * '=')
                    if filtered_packets != EMPTY_LIST:
                        for rpacket in filtered_packets[0:3]:
                            for key, val in rpacket.items():
                                print(f"{DEBUG_HEADER} {key}={val}")

                        for rpacket in filtered_packets[-4:-1]:
                            for key, val in rpacket.items():
                                print(f"{DEBUG_HEADER} {key}={val}")

                ################################ INSERT MEASURE ONLY IF THERE ARE NEW MEASUREMENTS ################################
                if filtered_packets != EMPTY_LIST:

                    ################################ RESHAPE API PACKET FOR INSERT MEASURE IN DATABASE #####################
                    reshaper = API2DatabaseReshaperFactory().create_api2database_reshaper(bot_personality = sc.PERSONALITY)
                    reshaped_packets = reshaper.reshape_packets(packets = filtered_packets,
                                                                reshape_mapping = measure_param_map)

                    if sc.DEBUG_MODE:
                        print(20 * "=" + " RESHAPED PACKETS " + 20 * '=')
                        if reshaped_packets != EMPTY_LIST:
                            for rpacket in reshaped_packets[0:3]:
                                for key, val in rpacket.items():
                                    print(f"{DEBUG_HEADER} {key}={val}")

                            for rpacket in reshaped_packets[-4:-1]:
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

                ################# END OF THE LOOP: ADD ONE DAY TO THE CURRENT FROM DATE ########################
                from_datetime = DatetimeParser.add_days_to_datetime(ts = from_datetime, days = 1)

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
