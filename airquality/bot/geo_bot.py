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
from airquality.mapper.packet_mapper import PacketMapper
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.api.urllib_adapter import UrllibAdapter

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, INFO_HEADER


################################ GEO BOT ABSTRACT BASE CLASS ################################
class GeoBot:

    def __init__(self,
                 dbconn,
                 url_builder_class,
                 file_parser_class,
                 reshaper_class,
                 packet_mapper_class=PacketMapper):
        self.dbconn = dbconn
        self.url_builder_class = url_builder_class
        self.file_parser_class = file_parser_class
        self.reshaper_class = reshaper_class
        self.packet_mapper_class = packet_mapper_class

    def run(self, url_builder_param: Dict[str, Any], active_locations: Dict[str, Any]):

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

            mapped_packets = []
            for packet in reshaped_packets:
                mapped_packets.append(packet_mapper.reshape(packet))

            if sc.DEBUG_MODE:
                print(20 * "=" + " MAPPED PACKETS " + 20 * '=')
                for packet in mapped_packets:
                    print(30 * '*')
                    for key, val in packet.items():
                        print(f"{DEBUG_HEADER} {key}={val}")

            ############## COMPARE THE OLD LOCATIONS WITH THE NEW DOWNLOADED FROM THE API ###################
            for name in new_locations.keys():
                if name in active_locations.keys():
                    # compare the locations
                    if new_locations[name] != active_locations[name]:

                        # update the old location 'valid_to' timestamp
                        ts = DatetimeParser.current_sqltimestamp()
                        query = query_builder.update_valid_to_timestamp_location(timestamp=ts, sensor_id=sensorname2id_map[name])
                        dbconn.send(executable_sql_query=query)

                        # insert new record corresponding to the sensor_id with the
                        query_statement = query_builder.insert_into_sensor_at_location()
                        query_statement += f"({sensorname2id_map[name]}, '{ts}', ST_GeomFromText('{new_locations[name]}', 26918));"
                        dbconn.send(executable_sql_query=query_statement)

                    else:
                        print(f"{INFO_HEADER} old_location='{active_locations[name]}' is equal to new_location='{new_locations[name]}'")
                else:
                    print(f"{INFO_HEADER} name='{name}' is not an active locations...")
        else:
            print(f"{INFO_HEADER} empty packets.")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
