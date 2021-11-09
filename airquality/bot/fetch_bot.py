#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 11:33
# @Description: this script defines the bot classes for the fetch module
#
#################################################
from typing import Dict, Any, List

# IMPORT GLOBAL VARIABLE FROM FETCH MODULE
import airquality.constants.system_constants as sc

# IMPORT CLASSES FROM AIRQUALITY MODULE
from data.builder.url import URLBuilder
from io.remote.api.adapter import UrllibAdapter
from utility.datetime_parser import DatetimeParser
from data.reshaper.packet import PacketReshaper
from utility.db_answer_parser import DatabaseAnswerParser
from data.reshaper.uniform.db2api import UniversalAPIAdapter
from data.reshaper.uniform.api2db import UniversalDatabaseAdapter

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, EXCEPTION_HEADER, INFO_HEADER, WARNING_HEADER


class FetchBot:

    def __init__(self,
                 dbconn,
                 file_parser_class,
                 url_builder_class=URLBuilder,
                 packet_reshaper_class=PacketReshaper,
                 universal_api_adapter_class=UniversalAPIAdapter,
                 universal_db_adapter_class=UniversalDatabaseAdapter):
        self.dbconn = dbconn
        self.file_parser_class = file_parser_class
        self.url_builder_class = url_builder_class
        self.packet_reshaper_class = packet_reshaper_class
        self.universal_api_adapter_class = universal_api_adapter_class
        self.universal_db_adapter_class = universal_db_adapter_class

    def run(self,
            api_address: str,
            url_param: Dict[str, Any],
            sensor_ids: List[int],
            select_apiparam_query: str):

        ################################ DEFINE ALL VARIABLES USED BELOW ################################
        universal_db_adapter = self.universal_db_adapter_class()
        universal_api_adapter = self.universal_api_adapter_class()
        packet_reshaper = self.packet_reshaper_class()
        file_parser = self.file_parser_class()
        filter_sqltimestamp = "2021-11-08 20:00:00"

        ################################ CYCLE ON EACH SENSOR ################################
        for sensor_id in sensor_ids:
            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT API PARAM FROM DATABASE ################################
            query = select_apiparam_query.format(sensor_id=sensor_id)
            answer = self.dbconn.send(executable_sql_query=query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            if not api_param:
                raise SystemExit(f"{EXCEPTION_HEADER} {FetchBot.__name__} fetched API param for sensor_id={sensor_id} "
                                 f"but are empty.")

            ################################ UNIVERSAL API PARAMETERS ################################
            universal_api_param = universal_api_adapter.adapt(api_param)

            ############################# CYCLE ON UNIVERSAL API PARAM OF A SINGLE SENSOR ##############################
            for api_param in universal_api_param:

                ################################ MERGE TOGETHER ALL URL PARAMETERS ################################
                url_param.update(api_param)

                if sc.DEBUG_MODE:
                    print(20 * "=" + " URL PARAMETERS " + 20 * '=')
                    for key, val in url_param.items():
                        print(f"{DEBUG_HEADER} {key}={val}")

                ################################ FETCH DATA FROM API ################################
                url_builder = self.url_builder_class(api_address=api_address, parameters=url_param)
                url = url_builder.url()
                raw_api_packets = UrllibAdapter.fetch(url)
                parsed_api_packets = file_parser.parse(raw_api_packets)

                if sc.DEBUG_MODE:
                    print(f"{DEBUG_HEADER} {url}")

                ################################ RESHAPED PACKETS ################################
                reshaped_packets = packet_reshaper.reshape_packet(parsed_api_packets)

                if reshaped_packets:

                    ################################ ADAPT PACKETS FOR DATABASE ################################
                    universal_db_packets = []
                    for packet in reshaped_packets:
                        universal_db_packets.append(universal_db_adapter.adapt(packet))

                    ################################ FILTER PACKETS ################################
                    if sc.DEBUG_MODE:
                        print(20 * "=" + " FILTER MEASUREMENTS " + 20 * '=')
                    filtered_universal_packets = []
                    for universal_packet in universal_db_packets:
                        if DatetimeParser.is_ts2_after_ts1(ts2=universal_packet['timestamp'], ts1=filter_sqltimestamp):
                            filtered_universal_packets.append(universal_packet)
                        else:
                            print(f"{WARNING_HEADER} '{universal_packet['timestamp']}' => old measure")

                    if filtered_universal_packets:

                        if sc.DEBUG_MODE:
                            print(20 * "=" + " FILTERED MEASUREMENTS " + 20 * '=')
                            for universal_packet in filtered_universal_packets:
                                print(f"{DEBUG_HEADER} time={universal_packet['timestamp']}")

                    else:
                        print(f"{INFO_HEADER} no new measurements for sensor_id={sensor_id}")
                else:
                    print(f"{INFO_HEADER} empty packets.")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
