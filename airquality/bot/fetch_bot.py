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
from airquality.container.sql_container import MobileMeasurementSQLContainer, StationMeasurementSQLContainer
from airquality.container.sql_container_factory import SQLContainerFactory
from airquality.geom.postgis_geometry import PostGISPoint
from airquality.adapter.geom_adapter import GeometryAdapterAtmotube
from airquality.adapter.measurement_adapter import MeasurementAdapterFactory, MeasurementAdapterAtmotube, \
    MeasurementAdapterThingspeak
from airquality.adapter.channel_adapter import ChannelAdapter
from airquality.container.fetch_container_factory import FetchContainerFactory
from airquality.container.fetch_container import ChannelContainer, ChannelContainerWithFormattableAddress
from airquality.adapter.fetch_adapter import FetchAdapterThingspeak, FetchAdapterFactory, FetchAdapterAtmotube
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.parser.datetime_parser import DatetimeParser
from picker.query_picker import QueryPicker
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

        # Create fetch adapter
        fetch_adapter_fact = FetchAdapterFactory(fetch_adapter_class=FetchAdapterThingspeak)
        fetch_adapter = fetch_adapter_fact.make_adapter()

        # Create FetchContainer factory
        fetch_container_fact = FetchContainerFactory(fetch_container_class=ChannelContainerWithFormattableAddress)

        # Create MeasurementAdapter factory
        measure_adapter_fact = MeasurementAdapterFactory(adapter_class=MeasurementAdapterThingspeak)
        measure_adapter = measure_adapter_fact.make_adapter(measure_param_map=measure_param_map)

        # StationMeasurementSQLContainer factory
        measure_container_fact = SQLContainerFactory(container_class=StationMeasurementSQLContainer)

        ####################### DEFINE START DATE AND STOP DATE FOR FETCHING DATA FROM API #####################
        stop_datetime = DatetimeParser.today()

        ################################ FOR EACH SENSOR DO THE STUFF BELOW ################################

        for sensor_id in sensor_ids:

            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT SENSOR API PARAM FROM DATABASE ################################
            query = query_builder.select_api_param_from_sensor_id(sensor_id=sensor_id)
            answer = dbconn.send(executable_sql_query=query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            # Reshape API param from all-in-one into single-channel param
            sensor2channel_reshaper = ChannelAdapter(api_param=api_param)
            single_channel_api_param = sensor2channel_reshaper.adapt()

            #
            # Now the packets are compliant to the interface => {'id', 'key', 'ts'}
            #

            # Adapt packets to a general interface that is decoupled by the sensor's API data structure
            channel_adapted_parameters = []
            for single_channel in single_channel_api_param:
                channel_adapted_parameters.append(fetch_adapter.adapt(packet=single_channel))

            #
            # Now the packets are compliant to the interface => {'channel_id', 'channel_key', 'channel_ts'}
            #

            if sc.DEBUG_MODE:
                print(20 * "=" + " CHANNEL ADAPTED PARAMETERS " + 20 * '=')
                for param in channel_adapted_parameters:
                    for api_key, api_val in param.items():
                        print(f"{DEBUG_HEADER} {api_key}={api_val}")

            # Create FetchContainers
            for channel_param in channel_adapted_parameters:

                # define from datetime
                from_datetime = DatetimeParser.string2datetime(datetime_string=channel_param['channel_ts']['val'])
                from_datetime = DatetimeParser.add_seconds_to_datetime(ts=from_datetime, seconds=3)

                # define to datetime
                to_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=7)

                if (to_datetime - stop_datetime).total_seconds() > 0:
                    to_datetime = stop_datetime

                # CONTINUE UNTIL TODAY IS REACHED
                while (stop_datetime - from_datetime).total_seconds() >= 0:

                    # Create a ChannelContainer object for building the api URL
                    channel_container = fetch_container_fact.make_container(parameters=channel_param)

                    # build URL
                    url = channel_container.url(api_address=api_address,
                                                optional_param={'end': DatetimeParser.datetime2string(to_datetime)})
                    if sc.DEBUG_MODE:
                        print(f"{DEBUG_HEADER} {url}")

                    # Fetch data from API (API packets)
                    api_packets = UrllibAdapter.fetch(url=url)
                    parser = FileParserFactory.file_parser_from_file_extension(file_extension="json")
                    parsed_api_packets = parser.parse(raw_string=api_packets)

                    # Reshape API packets: merge all data coming from different channels into a single PlainAPIPacket object
                    api_packet_reshaper = PacketReshaperFactory().make_reshaper(
                        bot_personality=sc.PERSONALITY)
                    reshaped_api_packets = api_packet_reshaper.reshape_packet(api_answer=parsed_api_packets)

                    if reshaped_api_packets:

                        adapted_packets = []
                        for packet in reshaped_api_packets:
                            packet['timestamp'] = DatetimeParser.thingspeak_to_sqltimestamp(packet['created_at'])
                            adapted_packet = measure_adapter.adapt(packet)
                            adapted_packets.append(adapted_packet)

                        # This method return a SQLContainerComposition object !!!
                        measure_container = measure_container_fact.make_container_with_sensor_id(
                            packets=adapted_packets, sensor_id=sensor_id
                        )

                        query_statement = query_builder.insert_into_station_measurements()
                        query = measure_container.sql(query=query_statement)
                        dbconn.send(executable_sql_query=query)

                        ###################### UPDATE LAST CHANNEL ACQUISITION TIMESTAMP #########################
                        if sc.DEBUG_MODE:
                            print(f"{INFO_HEADER} last {channel_param['ts_name']} => {adapted_packets[-1]['timestamp']}")

                        query = query_builder.update_last_channel_acquisition_timestamp(
                            sensor_id=sensor_id,
                            ts=adapted_packets[-1]['timestamp'],
                            param2update=channel_param['ts_name'])
                        dbconn.send(executable_sql_query=query)

                    else:
                        print(f"{INFO_HEADER} empty packets.")

                    ############################## INCREMENT THE PERIOD FOR DATA FETCHING ##############################
                    from_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=7)
                    channel_param['channel_ts']['val'] = DatetimeParser.datetime2string(from_datetime)
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
        api_answer_reshaper = PacketReshaperFactory().make_reshaper(
            bot_personality=sc.PERSONALITY)

        # Create measurement container adapter to adapt packets to a general SQLContainer interface
        measure_adapter_fact = MeasurementAdapterFactory(adapter_class=MeasurementAdapterAtmotube)
        measure_adapter = measure_adapter_fact.make_adapter(measure_param_map=measure_param_map)

        # Create GeometryAdapter
        geom_adapter_fact = GeometryAdapterFactory(geom_adapter_class=GeometryAdapterAtmotube)
        geom_adapter = geom_adapter_fact.make_geometry_adapter()

        # PostGIS geometry Factory
        postgis_geom_fact = PostGISGeometryFactory(geom_class=PostGISPoint)

        # MobileMeasurementSQLContainer factory
        measure_container_fact = SQLContainerFactory(container_class=MobileMeasurementSQLContainer)

        ################################ FOR EACH SENSOR DO THE STUFF BELOW ################################

        for sensor_id in sensor_ids:

            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT SENSOR's API PARAM FROM DATABASE ################################
            query = query_builder.select_api_param_from_sensor_id(sensor_id=sensor_id)
            answer = dbconn.send(executable_sql_query=query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            # Adapt packets to the general interface in order to decouple them from the sensor's specific API param name.
            channel_adapted_param = fetch_adapter.adapt(packet=api_param)

            ################################ CYCLE THROUGH DATE UNTIL NOW ################################
            stop_datetime = DatetimeParser.today()
            from_datetime = DatetimeParser.string2datetime(datetime_string=channel_adapted_param['channel_ts']['val'])
            filter_sqltimestamp = channel_adapted_param['channel_ts']['val']

            while (from_datetime - stop_datetime).total_seconds() < 0:

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

                if reshaped_api_answer:

                    # Adapt packets to mobile measurement SQL container interface
                    adapted_packets = []
                    for packet in reshaped_api_answer:
                        geom_adapted_packet = geom_adapter.adapt(packet=packet)
                        postgis_geom = postgis_geom_fact.create_geometry(param=geom_adapted_packet)
                        packet['geom'] = postgis_geom.get_database_string()
                        packet['timestamp'] = DatetimeParser.atmotube_to_sqltimestamp(ts=packet['time'])
                        adapted_packet = measure_adapter.adapt(packet=packet)
                        adapted_packets.append(adapted_packet)

                    # create a container filter to keep only the measurement from the last timestamp on
                    filtered_packets = []
                    for packet in adapted_packets:
                        if DatetimeParser.is_ts2_after_ts1(ts1=filter_sqltimestamp, ts2=packet['timestamp']):
                            filtered_packets.append(packet)

                    if filtered_packets:

                        if sc.DEBUG_MODE:
                            print(20 * "=" + " FILTERED PACKETS " + 20 * '=')
                            for packet in filtered_packets:
                                print(30 * '*')
                                for key, val in packet.items():
                                    print(f"{DEBUG_HEADER} {key}={val}")

                        # measure containers
                        measure_containers = measure_container_fact.make_container_with_sensor_id(
                            packets=adapted_packets, sensor_id=sensor_id
                        )

                        # Execute the query
                        query_statement = query_builder.insert_into_mobile_measurements()
                        query = measure_containers.sql(query=query_statement)
                        dbconn.send(executable_sql_query=query)

                        ############# UPDATE LAST MEASURE TIMESTAMP FOR KNOWING WHERE TO START WITH NEXT FETCH #############
                        if sc.DEBUG_MODE:
                            print(f"{INFO_HEADER} last_timestamp={adapted_packets[-1]['timestamp']}")

                        query = query_builder.update_last_packet_date_atmotube(
                            last_timestamp=adapted_packets[-1]['timestamp'],
                            sensor_id=sensor_id)
                        dbconn.send(executable_sql_query=query)

                    else:
                        print(f"{INFO_HEADER} all packets downloaded are already present into the database.")
                else:
                    print(f"{INFO_HEADER} empty packets.")

                ################# END OF THE LOOP: ADD ONE DAY TO THE CURRENT FROM DATE ########################
                from_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=1)
                channel_adapted_param['channel_ts']['val'] = DatetimeParser.datetime2string(from_datetime)

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
