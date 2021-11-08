######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 08/11/21 16:25
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

from typing import Dict, Any, List

# IMPORT GLOBAL VARIABLE FROM FETCH MODULE
import airquality.constants.system_constants as sc


# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.reshaper.packet_reshaper import PacketReshaper
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
from airquality.api.urllib_adapter import UrllibAdapter

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, INFO_HEADER, EXCEPTION_HEADER


class DateFetchBot:

    def __init__(self,
                 dbconn,
                 file_parser_class,
                 url_builder_class=URLBuilder,
                 packet_reshaper_class=PacketReshaper,
                 universal_api_adapter_class=UniversalAPIAdapter):
        self.dbconn = dbconn
        self.file_parser_class = file_parser_class
        self.url_builder_class = url_builder_class
        self.packet_reshaper_class = packet_reshaper_class
        self.universal_api_adapter_class = universal_api_adapter_class

    def run(self,
            api_address: str,
            url_param: Dict[str, Any],
            sensor_ids: List[int],
            select_apiparam_query: str):

        ################################ DEFINE ALL VARIABLES USED BELOW ################################
        packet_reshaper = self.packet_reshaper_class()
        file_parser = self.file_parser_class()          # file parser object for parsing packets fetched from API.
        stop_datetime = DatetimeParser.today()          # datetime object that indicates the bot when stop.

        ################################ CYCLE ON EACH SENSOR ################################
        for sensor_id in sensor_ids:
            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT API PARAM FROM DATABASE ################################
            query = select_apiparam_query.format(sensor_id=sensor_id)
            answer = self.dbconn.send(executable_sql_query=query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            if not api_param:
                raise SystemExit(f"{EXCEPTION_HEADER} {DateFetchBot.__name__} fetched API param for sensor_id={sensor_id} "
                                 f"but are empty.")

            ################################ UNIVERSAL API ADAPTER ################################
            universal_api_adapter = self.universal_api_adapter_class()
            universal_api_param = universal_api_adapter.adapt(api_param)

            ############################# CYCLE ON UNIVERSAL API PARAM OF A SINGLE SENSOR ##############################
            for api_param in universal_api_param:

                # from_datetime = DatetimeParser.string2datetime("2018-01-01 00:00:00")  # [ONLY FOR NOW]
                #
                # from_datetime = DatetimeParser.string2datetime(datetime_string=channel_param['channel_ts']['val'])
                # from_datetime = DatetimeParser.add_seconds_to_datetime(ts=from_datetime, seconds=3)
                #
                # # define to datetime
                # to_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=7)
                #
                # if (to_datetime - stop_datetime).total_seconds() > 0:
                #     to_datetime = stop_datetime
                #
                # # CONTINUE UNTIL TODAY IS REACHED
                # while (stop_datetime - from_datetime).total_seconds() >= 0:
                #

                # TODO: TAKE START AND STOP DATA FROM THE FILE FROM THE SENSOR_ID

                ################################ MERGE TOGETHER ALL URL PARAMETERS ################################
                url_param.update(api_param)

                # TODO: ADD ALSO TIMESTAMP PARAM TAKEN FROM THE FILE

                if sc.DEBUG_MODE:
                    print(20 * "=" + " URL PARAMETERS " + 20 * '=')
                    for key, val in url_param.items():
                        print(f"{DEBUG_HEADER} {key}={val}")

                ################################ FETCH DATA FROM API ################################
                url_builder = self.url_builder_class(api_address=api_address, parameters=url_param)
                url = url_builder.build_url()
                raw_api_packets = UrllibAdapter.fetch(url)
                parsed_api_packets = file_parser.parse(raw_api_packets)

                if sc.DEBUG_MODE:
                    print(f"{DEBUG_HEADER} {url}")

                ################################ RESHAPE PACKETS ################################
                reshaped_packets = packet_reshaper.reshape_packet(parsed_api_packets)

                if reshaped_packets:
                    if sc.DEBUG_MODE:
                        print(20 * "=" + " RESHAPED PACKETS " + 20 * '=')
                        for packet in reshaped_packets:
                            print(30 * '*')
                            for key, val in packet.items():
                                print(f"{DEBUG_HEADER} {key}={val}")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
