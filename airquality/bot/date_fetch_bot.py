######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 08/11/21 16:25
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

from typing import List

# IMPORT GLOBAL VARIABLE FROM FETCH MODULE
import airquality.constants.system_constants as sc


# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.api.url_builder import URLBuilder
from airquality.adapter.universal_api_adapter import UniversalAPIAdapter
from airquality.container.sql_container import MobileMeasurementSQLContainer, StationMeasurementSQLContainer
from airquality.container.sql_container_factory import SQLContainerFactory
from airquality.geom.postgis_geometry import PostGISPoint
from airquality.adapter.geom_adapter import GeometryAdapterAtmotube
from airquality.adapter.measurement_adapter import MeasurementAdapterFactory, MeasurementAdapterAtmotube, \
    MeasurementAdapterThingspeak
from airquality.adapter.channel_adapter import ChannelAdapter
from airquality.container.fetch_container_factory import FetchContainerFactory
from airquality.container.fetch_container import ChannelContainer, ChannelContainerWithFormattableAddress
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.parser.datetime_parser import DatetimeParser
from airquality.picker.query_picker import QueryPicker
from airquality.api.urllib_adapter import UrllibAdapter
from airquality.picker.json_param_picker import JSONParamPicker
from airquality.picker.api_param_picker import APIParamPicker
from airquality.picker.resource_picker import ResourcePicker
from airquality.parser.file_parser import FileParserFactory

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, INFO_HEADER, EXCEPTION_HEADER


class DateFetchBot:

    def __init__(self,
                 dbconn,
                 url_builder_class=URLBuilder,
                 universal_api_adapter_class=UniversalAPIAdapter):
        self.dbconn = dbconn
        self.url_builder_class = url_builder_class
        self.universal_api_adapter_class = universal_api_adapter_class

    def run(self,
            api_address: str,
            url_param: str,
            sensor_ids: List[int],
            select_apiparam_query: str):

        for sensor_id in sensor_ids:
            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT API PARAM FROM DATABASE ################################
            query = select_apiparam_query.format(sensor_id=sensor_id)
            answer = self.dbconn.send(executable_sql_query=query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            if not api_param:
                raise SystemExit(f"{EXCEPTION_HEADER} {DateFetchBot.__name__} fetched API param but are empty.")

            ################################ UNIVERSAL API ADAPTER ################################
            universal_api_adapter = self.universal_api_adapter_class()
            universal_api_param = universal_api_adapter.adapt(api_param)

            if sc.DEBUG_MODE:
                print(20 * "=" + " UNIVERSAL API PARAMETERS " + 20 * '=')
                for api_param in universal_api_param:
                    print(30*"*")
                    for key, val in api_param.items():
                        print(f"{DEBUG_HEADER} {key}={val!s}")

            ############################# CYCLE ON UNIVERSAL API PARAM OF A SINGLE SENSOR ##############################
            for api_param in universal_api_param:

                # TODO: TAKE START AND STOP DATA FROM THE FILE

                # define from datetime
                # from_datetime = DatetimeParser.string2datetime(datetime_string=channel_param['channel_ts']['val'])
                # from_datetime = DatetimeParser.add_seconds_to_datetime(ts=from_datetime, seconds=3)
                #
                # # define to datetime
                # to_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=7)
                #
                # if (to_datetime - stop_datetime).total_seconds() > 0:
                #     to_datetime = stop_datetime

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


        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
