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
from airquality.geom.postgis_geometry import PostGISGeometryFactory, PostGISPoint
from airquality.adapter.geom_adapter import GeometryAdapterFactory, GeometryAdapterAtmotube
from airquality.adapter.measurement_adapter import MeasurementAdapterFactory, MeasurementAdapterAtmotube
from airquality.reshaper.api_packet_reshaper import APIPacketReshaperFactory
from airquality.adapter.channel_adapter import ChannelAdapter
from airquality.container.fetch_container_factory import FetchContainerFactory
from airquality.container.fetch_container import ChannelContainer, ChannelContainerWithFormattableAddress
from airquality.adapter.fetch_adapter import FetchAdapterThingspeak, FetchAdapterFactory, FetchAdapterAtmotube
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.parser.datetime_parser import DatetimeParser
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.api.urllib_adapter import UrllibAdapter
from airquality.picker.json_param_picker import JSONParamPicker
from airquality.picker.api_param_picker import APIParamPicker
from airquality.picker.resource_picker import ResourcePicker
from airquality.parser.file_parser import FileParserFactory
from airquality.io.io import IOManager

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, DEBUG_HEADER, INFO_HEADER, \
    PURPLEAIR_PERSONALITY


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
        raw_query_data = IOManager.open_read_close_file(path=QUERY_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=QUERY_FILE.split('.')[-1])
        parsed_query_data = parser.parse(raw_string=raw_query_data)
        query_builder = SQLQueryBuilder(parsed_query_data)

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

        ################################ SELECT SENSOR IDS FROM PERSONALITY ################################
        query = query_builder.select_sensor_ids_from_personality(personality=PURPLEAIR_PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensor_ids = DatabaseAnswerParser.parse_single_attribute_answer(response=answer)

        ################################ IF THERE ARE NO SENSORS, THE PROGRAM STOPS HERE ###############################
        if not sensor_ids:
            print(f"{INFO_HEADER} no sensor found for personality='{PURPLEAIR_PERSONALITY}'.")
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

        ####################### CREATE QUERYSTRING OPTIONAL PARAMETERS DICTIONARY #####################
        optional_param = {}  # no optional parameters for ThingSpeak bot

        ################################ FOR EACH SENSOR DO THE STUFF BELOW ################################

        for sensor_id in sensor_ids:

            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT SENSOR API PARAM FROM DATABASE ################################
            query = query_builder.select_api_param_from_sensor_id(sensor_id=sensor_id)
            answer = dbconn.send(executable_sql_query=query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            # Reshape API param from all-in-one into single-channel param
            sensor2channel_reshaper = ChannelAdapter(api_param=api_param)
            single_channel_api_param = sensor2channel_reshaper.reshape()

            #
            # Now the packets are compliant to the interface => {'id', 'key', 'ts'}
            #

            # Create fetch adapter
            fetch_adapter_fact = FetchAdapterFactory(fetch_adapter_class=FetchAdapterThingspeak)
            fetch_adapter = fetch_adapter_fact.make_adapter()

            # Adapt packets to a general interface that is decoupled by the sensor's API data structure
            channel_adapted_parameters = []
            for single_channel in single_channel_api_param:
                channel_adapted_parameters.append(fetch_adapter.adapt_packet(packet=single_channel))

            #
            # Now the packets are compliant to the interface => {'channel_id', 'channel_key', 'channel_ts'}
            #

            if sc.DEBUG_MODE:
                print(20 * "=" + " CHANNEL ADAPTED PARAMETERS " + 20 * '=')
                for param in channel_adapted_parameters:
                    for api_key, api_val in param.items():
                        print(f"{DEBUG_HEADER} {api_key}={api_val}")

            # Create FetchContainer
            fetch_container_fact = FetchContainerFactory(fetch_container_class=ChannelContainerWithFormattableAddress)
            channel_containers = []
            for channel_param in channel_adapted_parameters:
                channel_containers.append(fetch_container_fact.make_container(parameters=channel_param))

            # Make URL from container
            for channel in channel_containers:
                url = channel.url(api_address=api_address, optional_param=optional_param)
                if sc.DEBUG_MODE:
                    print(f"{DEBUG_HEADER} {url}")

            # # Cycle on channels
            # for channel in reshaped_channels:
            #
            #     ####################### DEFINE START DATE AND STOP DATE FOR FETCHING DATA FROM API #####################
            #     stop_datetime = DatetimeParser.today()
            #     from_datetime = DatetimeParser.string2datetime(datetime_string=THINGSPEAK_START_FETCH_TIMESTAMP)
            #
            #     # CHECK IF THERE ARE MEASUREMENTS ALREADY PRESENT INTO THE DATABASE FOR THE GIVEN CHANNEL_ID
            #     if channel.channel_ts != 'null':
            #         from_datetime = DatetimeParser.string2datetime(datetime_string=channel.channel_ts)
            #         from_datetime = DatetimeParser.add_seconds_to_datetime(ts=from_datetime, seconds=3)
            #
            #     to_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=7)
            #     if (to_datetime - stop_datetime).total_seconds() > 0:
            #         to_datetime = stop_datetime
            #
            #     # CONTINUE UNTIL TODAY IS REACHED
            #     while (stop_datetime - from_datetime).total_seconds() >= 0:
            #
            #         # Format API address
            #         formatted_api_address = api_address.format(channel_id=channel.channel_id)
            #         if sc.DEBUG_MODE:
            #             print(20 * "=" + " API ADDRESS " + 20 * '=')
            #             print(f"{DEBUG_HEADER} {formatted_api_address}")
            #
            #         # api request adapter
            #         api_adapter = APIRequestAdapter(api_address=formatted_api_address)
            #
            #         # GET QUERYSTRING PARAMETERS
            #         querystring_param = {'api_key': channel.channel_key,
            #                              'start': DatetimeParser.datetime2string(ts=from_datetime),
            #                              'end': DatetimeParser.datetime2string(ts=to_datetime)}
            #
            #         # Build URL querystring
            #         querystring = querystring_builder.make_querystring(parameters=querystring_param)
            #         if sc.DEBUG_MODE:
            #             print(20 * "=" + " URL QUERYSTRING " + 20 * '=')
            #             print(f"{DEBUG_HEADER} {querystring}")
            #
            #         # Fetch data from API (API packets)
            #         api_packets = api_adapter.fetch(querystring)
            #         parser = FileParserFactory.file_parser_from_file_extension(file_extension="json")
            #         parsed_api_packets = parser.parse(raw_string=api_packets)
            #
            #         # Reshape API packets: merge all data coming from different channels into a single PlainAPIPacket object
            #         api_packet_reshaper = APIPacketReshaperFactory().create_api_packet_reshaper(bot_personality=sc.PERSONALITY)
            #         reshaped_api_packets = api_packet_reshaper.reshape_packet(api_answer=parsed_api_packets)
            #
            #         if sc.DEBUG_MODE:
            #             if reshaped_api_packets != EMPTY_LIST:
            #                 print(20 * "=" + " RESHAPED SINGLE CHANNEL API PACKETS " + 20 * '=')
            #                 for packet in reshaped_api_packets[0:3]:
            #                     print(f"{DEBUG_HEADER} {str(packet)}")
            #
            #                 for packet in reshaped_api_packets[-4:-1]:
            #                     print(f"{DEBUG_HEADER} {str(packet)}")
            #
            #         ####################### DO THE INSERT AND UPDATE ONLY IF PACKETS ARE PRESENT #####################
            #         if reshaped_api_packets:
            #
            #             # Create a station packet wrapper for decoding api packets into sql wrapper packets
            #             station_packet_wrapper = wrapper_factory.create_packet_wrapper(bot_personality=sc.PERSONALITY,
            #                                                                            mapping=measure_param_map,
            #                                                                            sensor_id=sensor_id)
            #
            #             # got a list of SQL wrapper station packet(s)
            #             wrapped_packets = station_packet_wrapper.decode_packets(packets=reshaped_api_packets)
            #
            #             if sc.DEBUG_MODE:
            #                 if wrapped_packets != EMPTY_LIST:
            #                     print(20 * "=" + " SQL WRAPPER STATION PACKETS " + 20 * '=')
            #                     for packet in wrapped_packets[0:3]:
            #                         print(f"{DEBUG_HEADER} {str(packet)}")
            #
            #                     for packet in wrapped_packets[-4:-1]:
            #                         print(f"{DEBUG_HEADER} {str(packet)}")
            #
            #             # Create a Bridge object for inserting packets
            #             bridge = BridgeObject(packets=wrapped_packets)
            #             query = query_builder.insert_into_station_measurements(bridge=bridge)
            #             dbconn.send(executable_sql_query=query)
            #
            #             ###################### UPDATE LAST CHANNEL ACQUISITION TIMESTAMP #########################
            #             if sc.DEBUG_MODE:
            #                 print(f"{DEBUG_HEADER} last {channel.ts_name} = {reshaped_api_packets[-1].created_at}")
            #
            #             query = query_builder.update_last_channel_acquisition_timestamp(
            #                 sensor_id=sensor_id,
            #                 ts=reshaped_api_packets[-1].created_at,
            #                 param2update=channel.ts_name)
            #             dbconn.send(executable_sql_query=query)
            #
            #         ############################## INCREMENT THE PERIOD FOR DATA FETCHING ##############################
            #         from_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=7)
            #         to_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=7)
            #
            #         if (to_datetime - stop_datetime).total_seconds() >= 0:
            #             to_datetime = stop_datetime

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
        raw_query_data = IOManager.open_read_close_file(path=QUERY_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=QUERY_FILE.split('.')[-1])
        parsed_query_data = parser.parse(raw_string=raw_query_data)
        query_builder = SQLQueryBuilder(parsed_query_data)

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

        ##################### SELECT SENSOR IDS ASSOCIATED TO CURRENT PERSONALITY (ATMOTUBE) ###########################
        query = query_builder.select_sensor_ids_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensor_ids = DatabaseAnswerParser.parse_single_attribute_answer(response=answer)

        ################################ IF THERE ARE NO SENSORS, THE PROGRAM STOPS HERE ###############################
        if not sensor_ids:
            print(f"{INFO_HEADER} no sensor found for personality='{sc.PERSONALITY}'.")
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

        ############### CREATE OPTIONAL API PARAMETERS ###################
        api_param2pick = ResourcePicker.pick_optional_api_parameters_from_api_data(personality=sc.PERSONALITY)
        optional_param = APIParamPicker.pick_param(api_param=parsed_api_data[sc.PERSONALITY],
                                                   param2pick=api_param2pick)

        if sc.DEBUG_MODE:
            print(20 * "=" + " OPTIONAL API PARAMETERS " + 20 * '=')
            for key, val in optional_param.items():
                print(f"{DEBUG_HEADER} {key}={val}")

        ################################ INITIALIZE FACTORIES ################################
        # Create FetchAdapter for adapting packets
        fetch_adapter_fact = FetchAdapterFactory(fetch_adapter_class=FetchAdapterAtmotube)
        fetch_adapter = fetch_adapter_fact.make_adapter()

        # FetchContainer factory
        fetch_container_fact = FetchContainerFactory(fetch_container_class=ChannelContainer)

        # API answer reshaper factory
        api_answer_reshaper = APIPacketReshaperFactory().create_api_packet_reshaper(
            bot_personality=sc.PERSONALITY)

        # Create measurement container adapter to adapt packets to a general SQLContainer interface
        measure_adapter_fact = MeasurementAdapterFactory(adapter_class=MeasurementAdapterAtmotube)
        measure_adapter = measure_adapter_fact.make_adapter(measure_param_map=measure_param_map)

        # Create GeometryAdapter
        geom_adapter_fact = GeometryAdapterFactory(geom_adapter_class=GeometryAdapterAtmotube)
        geom_adapter = geom_adapter_fact.make_geometry_adapter()

        # PostGIS geometry Factory
        postgis_geom_fact = PostGISGeometryFactory(geom_class=PostGISPoint)

        ################################ FOR EACH SENSOR DO THE STUFF BELOW ################################

        for sensor_id in sensor_ids:

            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT SENSOR's API PARAM FROM DATABASE ################################
            query = query_builder.select_api_param_from_sensor_id(sensor_id=sensor_id)
            answer = dbconn.send(executable_sql_query=query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            ################################ CYCLE THROUGH DATE UNTIL NOW ################################
            stop_datetime = DatetimeParser.today()
            from_datetime = DatetimeParser.string2datetime(datetime_string=api_param['date'])
            filter_sqltimestamp = api_param['date']

            while (from_datetime - stop_datetime).total_seconds() < 0:

                # Adapt packets to the general interface in order to decouple them from the sensor's specific API param name.
                channel_adapted_param = fetch_adapter.adapt_packet(packet=api_param)

                if sc.DEBUG_MODE:
                    print(20 * "=" + " CHANNEL ADAPTED PACKETS " + 20 * '=')
                    for api_key, api_val in channel_adapted_param.items():
                        print(f"{DEBUG_HEADER} {api_key}={api_val}")

                ############### CREATE FETCH CONTAINER ###################
                channel_container = fetch_container_fact.make_container(parameters=channel_adapted_param)

                url = channel_container.url(api_address=api_address, optional_param=optional_param)
                if sc.DEBUG_MODE:
                    print(20 * "=" + " URL " + 20 * '=')
                    print(f"{DEBUG_HEADER} {url}")

                ################################ FETCH DATA FROM API ################################
                api_answer = UrllibAdapter.fetch(url=url)
                parser = FileParserFactory.file_parser_from_file_extension(file_extension="json")
                api_answer = parser.parse(raw_string=api_answer)

                ########## RESHAPE THE API ANSWER INTO AN INTERFACE COMPLIANT TO SQL CONTAINER ################
                reshaped_api_answer = api_answer_reshaper.reshape_packet(api_answer=api_answer)

                if sc.DEBUG_MODE:
                    print(20 * "=" + " RESHAPED API PACKETS " + 20 * '=')
                    for packet in reshaped_api_answer:
                        print(30 * '*')
                        for key, val in packet.items():
                            print(f"{DEBUG_HEADER} {key}={val}")

                # Adapt packets to mobile measurement SQL container interface
                adapted_packets = []
                for packet in reshaped_api_answer:
                    geom_adapted_packet = geom_adapter.adapt_packet(packet=packet)
                    postgis_geom = postgis_geom_fact.create_geometry(param=geom_adapted_packet)
                    packet['geom'] = postgis_geom.get_database_string()
                    packet['timestamp'] = DatetimeParser.atmotube_to_sqltimestamp(ts=packet['time'])
                    adapted_packet = measure_adapter.adapt_packets(packet=packet)
                    adapted_packets.append(adapted_packet)

                if sc.DEBUG_MODE:
                    print(20 * "=" + " ADAPTED API PACKETS " + 20 * '=')
                    for packet in adapted_packets:
                        for key, val in packet.items():
                            print(f"{DEBUG_HEADER} {key}={val}")







            #     ################# FILTER PACKETS ONLY IF IT IS NOT THE FIRST ACQUISITION FOR THE SENSOR ################
            #     filtered_packets = datetime_filter.filter_packets(packets=plain_packets, sqltimestamp=filter_sqltimestamp)
            #
            #     if sc.DEBUG_MODE:
            #         print(20 * "=" + " FILTERED PACKETS " + 20 * '=')
            #         if filtered_packets != EMPTY_LIST:
            #             for packet in filtered_packets[0:3]:
            #                 print(f"{DEBUG_HEADER} {str(packet)}")
            #
            #             for packet in filtered_packets[-4:-1]:
            #                 print(f"{DEBUG_HEADER} {packet}")
            #
            #     ########################### INSERT MEASURE ONLY IF THERE ARE NEW MEASUREMENTS ##########################
            #     if filtered_packets:
            #
            #         mobile_packets = []
            #         for packet in filtered_packets:
            #             mobile_packets.append(SQLWrapperMobilePacketAtmotube(mapping=measure_param_map, packet=packet))
            #
            #         if sc.DEBUG_MODE:
            #             print(20 * "=" + " SQL WRAPPER MOBILE PACKETS " + 20 * '=')
            #             for packet in mobile_packets[0:3]:
            #                 print(f"{DEBUG_HEADER} {str(packet)}")
            #
            #             for packet in mobile_packets[-4:-1]:
            #                 print(f"{DEBUG_HEADER} {packet}")
            #
            #         bridge = BridgeObject(packets=mobile_packets)
            #         query = query_builder.insert_into_mobile_measurements(bridge)
            #         dbconn.send(executable_sql_query=query)
            #
            #         ############# UPDATE LAST MEASURE TIMESTAMP FOR KNOWING WHERE TO START WITH NEXT FETCH #############
            #         if sc.DEBUG_MODE:
            #             print(f"{DEBUG_HEADER} last timestamp = {filtered_packets[-1].time}")
            #
            #         query = query_builder.update_last_packet_date_atmotube(
            #             last_timestamp=filtered_packets[-1].time,
            #             sensor_id=sensor_id)
            #         dbconn.send(executable_sql_query=query)
            #
            #     ################# END OF THE LOOP: ADD ONE DAY TO THE CURRENT FROM DATE ########################
            #     from_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=1)

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
