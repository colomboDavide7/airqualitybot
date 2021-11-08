#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 11:21
# @Description: this script defines the classes for running the geo bot
#
#################################################
from typing import Dict, Any

# IMPORT GLOBAL VARIABLE FROM FETCH MODULE
import airquality.constants.system_constants as sc

# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.parser.datetime_parser import DatetimeParser
from airquality.reshaper.packet_reshaper import PacketReshaper
from airquality.mapper.packet_mapper import PacketMapper
from airquality.api.urllib_adapter import UrllibAdapter

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, INFO_HEADER, WARNING_HEADER


################################ GEO BOT ABSTRACT BASE CLASS ################################
class GeoBot:

    def __init__(self,
                 dbconn,
                 url_builder_class,
                 file_parser_class,
                 reshaper_class=PacketReshaper,
                 packet_mapper_class=PacketMapper):
        self.dbconn = dbconn
        self.url_builder_class = url_builder_class
        self.file_parser_class = file_parser_class
        self.reshaper_class = reshaper_class
        self.packet_mapper_class = packet_mapper_class

    def run(self,
            url_builder_param: Dict[str, Any],
            active_locations: Dict[str, Any],
            name2id_map: Dict[str, Any],
            update_valid_to_timestamp: str,
            insert_into_sensor_at_location: str):

        ################################ API DATA FETCHING ################################
        url_builder = self.url_builder_class()  # instance for building URL
        url = url_builder.build_url(url_builder_param)  # the URL used for fetching data
        raw_packets = UrllibAdapter.fetch(url)  # raw packets fetched from API (json)
        parser = self.file_parser_class()  # instance for parsing the content
        parsed_packets = parser.parse(raw_packets)  # parsed packets fetched from API (dict)

        ################################ RESHAPE PACKETS ################################
        packet_reshaper = self.reshaper_class()
        reshaped_packets = packet_reshaper.reshape_packet(parsed_packets)

        if reshaped_packets:

            if sc.DEBUG_MODE:
                print(20 * "=" + " RESHAPED PACKETS " + 20 * '=')
                for packet in reshaped_packets:
                    print(30 * '*')
                    for key, val in packet.items():
                        print(f"{DEBUG_HEADER} {key}={val}")

            ############################## PACKET MAPPER #############################
            packet_mapper = self.packet_mapper_class()
            mapped_packets = packet_mapper.reshape(reshaped_packets)

            if sc.DEBUG_MODE:
                print(20 * "=" + " MAPPED PACKETS " + 20 * '=')
                for key, val in mapped_packets.items():
                    print(f"{DEBUG_HEADER} {key}={val}")

            ############## COMPARE THE OLD LOCATIONS WITH THE NEW DOWNLOADED FROM THE API ###################
            for name in mapped_packets.keys():
                if name in active_locations.keys():
                    # compare the locations
                    if mapped_packets[name] != active_locations[name]:

                        # update the old location 'valid_to' timestamp
                        ts = DatetimeParser.current_sqltimestamp()
                        query = update_valid_to_timestamp.format(ts=ts, sens_id=name2id_map[name])
                        self.dbconn.send(executable_sql_query=query)

                        # insert new record corresponding to the sensor_id with the
                        query_statement = insert_into_sensor_at_location
                        query_statement += f"({name2id_map[name]}, '{ts}', ST_GeomFromText('{mapped_packets[name]}', 26918));"
                        self.dbconn.send(executable_sql_query=query_statement)

                    else:
                        print(f"{INFO_HEADER} old_location='{active_locations[name]}' is equal to "
                              f"new_location='{mapped_packets[name]}'.")
                else:
                    print(f"{WARNING_HEADER} name='{name}' is not an active locations...")
        else:
            print(f"{INFO_HEADER} empty packets.")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
