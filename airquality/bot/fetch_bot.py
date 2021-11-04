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
from airquality.plain.plain_api_param import PlainAPIParamThingspeak
from airquality.bridge.bridge_object import BridgeObject
from airquality.sqlwrapper.sql_wrapper_mobile_packet import SQLWrapperMobilePacketAtmotube
from airquality.reshaper.dict2stationpacket_reshaper import Dict2StationpacketReshaperFactory
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.filter.datetime_packet_filter import DatetimePacketFilterFactory
from airquality.api.url_querystring_builder import URLQuerystringBuilderFactory
from airquality.reshaper.api_packet_reshaper import APIPacketReshaperFactory
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

        ################################ QUERYSTRING BUILDER ################################
        querystring_builder = URLQuerystringBuilderFactory().create_querystring_builder(bot_personality=sc.PERSONALITY)

        ################################ SELECT SENSOR IDS FROM PERSONALITY ################################
        query = query_builder.select_sensor_ids_from_personality(personality=PURPLEAIR_PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensor_ids = DatabaseAnswerParser.parse_single_attribute_answer(response=answer)

        ################################ IF THERE ARE NO SENSORS, THE PROGRAM STOPS HERE ###############################
        if not sensor_ids:
            if sc.DEBUG_MODE:
                print(f"{DEBUG_HEADER} no sensor associated to personality = '{PURPLEAIR_PERSONALITY}'.")
            dbconn.close_conn()
            return

        if sc.DEBUG_MODE:
            print(20 * "=" + " DATABASE SENSOR IDS " + 20 * '=')
            for sensor_id in sensor_ids:
                print(f"{DEBUG_HEADER} {sensor_id}")

        ################################ SELECT MEASURE PARAM FROM PERSONALITY ################################
        query = query_builder.select_measure_param_from_personality(personality=PURPLEAIR_PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        measure_param_map = DatabaseAnswerParser.parse_key_val_answer(answer)

        if sc.DEBUG_MODE:
            print(20 * "=" + " MEASURE PARAM MAPPING " + 20 * '=')
            for param_code, param_id in measure_param_map.items():
                print(f"{DEBUG_HEADER} {param_code}={param_id}")

        ################################ FOR EACH SENSOR DO THE STUFF BELOW ################################

        for sensor_id in sensor_ids:

            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT SENSOR API PARAM FROM DATABASE ################################
            query = query_builder.select_api_param_from_sensor_id(sensor_id=sensor_id)
            answer = dbconn.send(executable_sql_query=query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            ################### CONVERT INTO PLAIN API PARAM ########################
            plain_param = PlainAPIParamThingspeak(api_param=api_param)
            if sc.DEBUG_MODE:
                print(20 * "=" + " PLAIN API PARAM " + 20 * '=')
                print(f"{DEBUG_HEADER} {str(plain_param)}")

            ################### RESHAPE API DATA FOR GETTING THE COUPLE CHANNEL_ID: CHANNEL_KEY ########################
            db2api_reshaper = Database2APIReshaperFactory().create_reshaper(bot_personality=sc.PERSONALITY)
            reshaped_api_param = db2api_reshaper.reshape_data(api_param=api_param)

            if sc.DEBUG_MODE:
                print(20 * "=" + " RESHAPED API PARAM " + 20 * '=')
                for ch_id in reshaped_api_param.keys():
                    print(f"{DEBUG_HEADER} {ch_id}")
                    for key, val in reshaped_api_param[ch_id].items():
                        print(f"{DEBUG_HEADER} {key}={val}")

            ######################## FORMAT API ADDRESS AND BUILD QUERYSTRING FOR EACH CHANNEL #########################

            for channel_id in reshaped_api_param.keys():

                # FORMAT API ADDRESS WITH CHANNEL ID
                formatted_api_address = api_address.format(channel_id=channel_id)

                # CREATE API REQUEST ADAPTER
                api_adapter = APIRequestAdapter(api_address=formatted_api_address)
                if sc.DEBUG_MODE:
                    print(20 * "=" + " API ADDRESS " + 20 * '=')
                    print(f"{DEBUG_HEADER} {formatted_api_address}")

                ####################### DEFINE START DATE AND STOP DATE FOR FETCHING DATA FROM API #####################

                stop_datetime = DatetimeParser.today()
                from_datetime = DatetimeParser.string2datetime(datetime_string=THINGSPEAK_START_FETCH_TIMESTAMP)

                # CHECK IF THERE ARE MEASUREMENTS ALREADY PRESENT INTO THE DATABASE FOR THE GIVEN CHANNEL_ID
                # ASSOCIATED TO THE SENSOR_ID
                if reshaped_api_param[channel_id].get('ts', None) is not None:
                    from_datetime = DatetimeParser.string2datetime(datetime_string=reshaped_api_param[channel_id]['ts'])

                to_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=7)
                if (to_datetime - stop_datetime).total_seconds() > 0:
                    to_datetime = stop_datetime

                # CONTINUE UNTIL TODAY IS REACHED
                while (stop_datetime - from_datetime).total_seconds() >= 0:

                    # GET QUERYSTRING PARAMETERS
                    querystring_param = {'api_key': reshaped_api_param[channel_id]['key'],
                                         'start': DatetimeParser.datetime2string(ts=from_datetime),
                                         'end': DatetimeParser.datetime2string(ts=to_datetime)}

                    # BUILD URL QUERYSTRING
                    querystring = querystring_builder.make_querystring(parameters=querystring_param)
                    if sc.DEBUG_MODE:
                        print(20 * "=" + " URL QUERYSTRING " + 20 * '=')
                        print(f"{DEBUG_HEADER} {querystring}")

                    # FETCH DATA FROM API
                    api_packets = api_adapter.fetch(querystring)
                    parser = FileParserFactory.file_parser_from_file_extension(file_extension="json")
                    parsed_api_packets = parser.parse(raw_string=api_packets)

                    # if sc.DEBUG_MODE:
                    #     print(20 * "=" + " API PACKETS " + 20 * '=')
                    #     if parsed_api_packets["feeds"] != EMPTY_LIST:
                    #         for i in range(3):
                    #             sqlwrapper = parsed_api_packets["feeds"][i]
                    #             for key, val in sqlwrapper.items():
                    #                 print(f"{DEBUG_HEADER} {key}={val}")

                    ####################### CONTINUE ONLY IF THERE ARE VALID PACKETS FROM APIS #########################
                    if parsed_api_packets["feeds"] != EMPTY_LIST:

                        ######### API PACKET RESHAPER FOR GETTING THE RIGHT MAPPING FOR NEXT INSERTION #################
                        api_packet_reshaper = APIPacketReshaperFactory().create_api_packet_reshaper(
                            bot_personality=sc.PERSONALITY)
                        reshaped_api_packets = api_packet_reshaper.reshape_packet(api_answer=parsed_api_packets)

                        # if sc.DEBUG_MODE:
                        #     if reshaped_api_packets != EMPTY_LIST:
                        #         print(20 * "=" + " RESHAPED API PACKETS " + 20 * '=')
                        #         for i in range(3):
                        #             sqlwrapper = reshaped_api_packets[i]
                        #             for key, val in sqlwrapper.items():
                        #                 print(f"{DEBUG_HEADER} {key}={val}")

                        ############### API 2 DATABASE RESHAPER FOR BUILDING THE QUERY LATER ###########################
                        api2db_reshaper = Dict2StationpacketReshaperFactory().create_reshaper(bot_personality=sc.PERSONALITY)
                        db_ready_packets = api2db_reshaper.reshape_packets(packets=reshaped_api_packets,
                                                                           measure_param_map=measure_param_map,
                                                                           sensor_id=sensor_id)

                        if sc.DEBUG_MODE:
                            if db_ready_packets != EMPTY_LIST:
                                print(20 * "=" + " DATABASE READY PACKETS " + 20 * '=')
                                for packet in db_ready_packets[0:3]:
                                    print(f"{DEBUG_HEADER} {str(packet)}")

                                for packet in db_ready_packets[-4:-1]:
                                    print(f"{DEBUG_HEADER} {str(packet)}")

                        ################# BUILD THE QUERY FOR INSERTING THE PACKETS INTO THE DATABASE ##################
                        query = query_builder.insert_into_station_measurements(packets=db_ready_packets)
                        dbconn.send(executable_sql_query=query)

                        ###################### UPDATE LAST CHANNEL ACQUISITION TIMESTAMP #########################
                        if sc.DEBUG_MODE:
                            print(f"{DEBUG_HEADER} last {reshaped_api_param[channel_id]['name']} = "
                                  f"{db_ready_packets[-1].timestamp}")

                        query = query_builder.update_last_channel_acquisition_timestamp(
                            sensor_id=sensor_id,
                            ts=db_ready_packets[-1].timestamp,
                            param2update=reshaped_api_param[channel_id]['name'])
                        dbconn.send(executable_sql_query=query)

                    ############################## INCREMENT THE PERIOD FOR DATA FETCHING ##############################
                    from_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=7)
                    to_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=7)

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

        ##################### SELECT SENSOR IDS ASSOCIATED TO CURRENT PERSONALITY (ATMOTUBE) ###########################
        query = query_builder.select_sensor_ids_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensor_ids = DatabaseAnswerParser.parse_single_attribute_answer(response=answer)

        ################################ IF THERE ARE NO SENSORS, THE PROGRAM STOPS HERE ###############################
        if sensor_ids == EMPTY_LIST:
            if sc.DEBUG_MODE:
                print(f"{DEBUG_HEADER} no sensor associated to personality = '{sc.PERSONALITY}'.")
            dbconn.close_conn()
            return

        if sc.DEBUG_MODE:
            print(20 * "=" + " DATABASE SENSOR IDS " + 20 * '=')
            for sensor_id in sensor_ids:
                print(f"{DEBUG_HEADER} {sensor_id}")

        ################################ SELECT MEASURE PARAM FROM IDENTIFIER ################################
        query = query_builder.select_measure_param_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        measure_param_map = DatabaseAnswerParser.parse_key_val_answer(answer)

        if sc.DEBUG_MODE:
            print(20 * "=" + " MEASURE PARAM MAPPING " + 20 * '=')
            for code, id_ in measure_param_map.items():
                print(f"{DEBUG_HEADER} {code}={id_}")

        # CREATE A DATETIME FILTER THAT WILL BE USED BELOW FOR FILTERING OUT PACKETS WHICH TIMESTAMP IS BEFORE
        # THE FILTER TIMESTAMP
        datetime_filter = DatetimePacketFilterFactory().create_datetime_filter(bot_personality=sc.PERSONALITY)

        ################################ FOR EACH SENSOR DO THE STUFF BELOW ################################

        for sensor_id in sensor_ids:

            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT SENSOR's API PARAM FROM DATABASE ################################
            query = query_builder.select_api_param_from_sensor_id(sensor_id=sensor_id)
            answer = dbconn.send(executable_sql_query=query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            if sc.DEBUG_MODE:
                print(20 * "=" + " API PARAMETERS " + 20 * '=')
                for name, value in api_param.items():
                    print(f"{DEBUG_HEADER} {name}={value}")

            ############### ADD OPTIONAL QUERYSTRING PARAMETER READ FROM API FILE ###################
            api_param2pick = ResourcePicker.pick_optional_api_parameters_from_api_data(personality=sc.PERSONALITY)
            optional_params = APIParamPicker.pick_param(api_param=parsed_api_data[sc.PERSONALITY],
                                                        param2pick=api_param2pick)

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
            querystring_builder = URLQuerystringBuilderFactory.create_querystring_builder(bot_personality=sc.PERSONALITY)

            ################################ CYCLE THROUGH DATE UNTIL NOW ################################
            stop_datetime = DatetimeParser.today()
            from_datetime = DatetimeParser.string2datetime(datetime_string=ATMOTUBE_START_FETCH_TIMESTAMP)

            # If api_param['date'] IS NOT NULL, use that value for filtering out packets in the same 'from_datetime'
            # but previous in time.
            filter_sqltimestamp = ""
            if api_param.get('date', None) is not None:
                from_datetime = DatetimeParser.string2datetime(datetime_string=api_param['date'])
                filter_sqltimestamp = api_param['date']

            while (from_datetime - stop_datetime).total_seconds() < 0:

                # INSERT DATETIME INTO API PARAMETERS
                from_datetime_string = DatetimeParser.datetime2string(ts=from_datetime)
                api_param['date'] = DatetimeParser.sqltimestamp_date(ts=from_datetime_string)

                # BUILD THE QUERYSTRING
                querystring = querystring_builder.make_querystring(parameters=api_param)

                if sc.DEBUG_MODE:
                    print(20 * "=" + " URL QUERYSTRING " + 20 * '=')
                    print(f"{DEBUG_HEADER} {querystring}")

                ################################ FETCH DATA FROM API ################################
                api_answer = api_adapter.fetch(querystring=querystring)
                parser = FileParserFactory.file_parser_from_file_extension(file_extension="json")
                api_answer = parser.parse(raw_string=api_answer)

                ################################ RESHAPE THE API ANSWER INTO PLAIN API PACKET ################################
                plain_reshaper = APIPacketReshaperFactory().create_api_packet_reshaper(bot_personality=sc.PERSONALITY)
                plain_packets = plain_reshaper.reshape_packet(api_answer=api_answer)

                if sc.DEBUG_MODE:
                    print(20 * "=" + " PLAIN PACKETS " + 20 * '=')
                    for packet in plain_packets[0:3]:
                        print(f"{DEBUG_HEADER} {str(packet)}")

                    for packet in plain_packets[-4:-1]:
                        print(f"{DEBUG_HEADER} {str(packet)}")

                ################# FILTER PACKETS ONLY IF IT IS NOT THE FIRST ACQUISITION FOR THE SENSOR ################
                filtered_packets = datetime_filter.filter_packets(packets=plain_packets, sqltimestamp=filter_sqltimestamp)

                if sc.DEBUG_MODE:
                    print(20 * "=" + " FILTERED PACKETS " + 20 * '=')
                    if filtered_packets != EMPTY_LIST:
                        for packet in filtered_packets[0:3]:
                            print(f"{DEBUG_HEADER} {str(packet)}")

                        for packet in filtered_packets[-4:-1]:
                            print(f"{DEBUG_HEADER} {packet}")

                ########################### INSERT MEASURE ONLY IF THERE ARE NEW MEASUREMENTS ##########################
                if filtered_packets:

                    mobile_packets = []
                    for packet in filtered_packets:
                        mobile_packets.append(SQLWrapperMobilePacketAtmotube(mapping=measure_param_map, packet=packet))

                    if sc.DEBUG_MODE:
                        print(20 * "=" + " SQL WRAPPER MOBILE PACKETS " + 20 * '=')
                        for packet in mobile_packets[0:3]:
                            print(f"{DEBUG_HEADER} {str(packet)}")

                        for packet in mobile_packets[-4:-1]:
                            print(f"{DEBUG_HEADER} {packet}")

                    bridge = BridgeObject(packets=mobile_packets)
                    query = query_builder.insert_into_mobile_measurements(bridge)
                    dbconn.send(executable_sql_query=query)

                    ############# UPDATE LAST MEASURE TIMESTAMP FOR KNOWING WHERE TO START WITH NEXT FETCH #############
                    if sc.DEBUG_MODE:
                        print(f"{DEBUG_HEADER} last timestamp = {filtered_packets[-1].time}")

                    query = query_builder.update_last_packet_date_atmotube(
                        last_timestamp=filtered_packets[-1].time,
                        sensor_id=sensor_id)
                    dbconn.send(executable_sql_query=query)

                ################# END OF THE LOOP: ADD ONE DAY TO THE CURRENT FROM DATE ########################
                from_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=1)

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
