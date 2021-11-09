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
import core.constants.system_constants as sc


# IMPORT CLASSES FROM AIRQUALITY MODULE
from data.builder.url import URLBuilder
from io.remote.api.adapter import UrllibAdapter
from data.builder.timest import DatetimeParser
from data.reshaper.packet import PacketReshaper
from data.reshaper.uniform.db2api import UniformReshaper


# IMPORT SHARED CONSTANTS
from core.constants.shared_constants import DEBUG_HEADER, EXCEPTION_HEADER


class DateFetchBot:

    def __init__(self,
                 dbconn,
                 file_parser_class,
                 url_builder_class=URLBuilder,
                 packet_reshaper_class=PacketReshaper,
                 universal_api_adapter_class=UniformReshaper):
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
        universal_api_adapter = self.universal_api_adapter_class()
        packet_reshaper = self.packet_reshaper_class()
        file_parser = self.file_parser_class()
        stop_datetime = DatetimeParser.today()

        ################################ CYCLE ON EACH SENSOR ################################
        for sensor_id in sensor_ids:
            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT API PARAM FROM DATABASE ################################
            query = select_apiparam_query.format(sensor_id=sensor_id)
            answer = self.dbconn.send(query=query)
            api_param = dict(answer)

            if not api_param:
                raise SystemExit(f"{EXCEPTION_HEADER} {DateFetchBot.__name__} fetched API param for sensor_id={sensor_id} "
                                 f"but are empty.")

            ################################ UNIVERSAL API ADAPTER ################################
            universal_api_param = universal_api_adapter.db2api(api_param)

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
                url = url_builder.url()
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
