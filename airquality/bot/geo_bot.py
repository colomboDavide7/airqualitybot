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
from data.builder.url import URLBuilder
from utility.query_picker import QueryPicker
from io.remote.api.adapter import UrllibAdapter
from data.builder.geom import GeometryBuilder
from utility.datetime_parser import DatetimeParser
from data.packet_reshaper import PacketReshaper
from data.universal_db_adapter import UniversalDatabaseAdapter
from data.builder.sql import GeoSQLContainer, SQLContainerComposition

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, INFO_HEADER, WARNING_HEADER


################################ GEO BOT ABSTRACT BASE CLASS ################################
class GeoBot:

    def __init__(self,
                 dbconn,
                 file_parser_class,
                 query_picker_instance: QueryPicker,
                 url_builder_class=URLBuilder,
                 reshaper_class=PacketReshaper,
                 universal_db_adapter_class=UniversalDatabaseAdapter,
                 geom_sqlcontainer_class=GeoSQLContainer,
                 composition_class=SQLContainerComposition,
                 postgis_geom_class=GeometryBuilder):
        self.dbconn = dbconn
        self.url_builder_class = url_builder_class
        self.file_parser_class = file_parser_class
        self.reshaper_class = reshaper_class
        self.universal_db_adapter_class = universal_db_adapter_class
        self.geo_sqlcontainer_class = geom_sqlcontainer_class
        self.composition_class = composition_class
        self.postgis_geom_class = postgis_geom_class
        self.query_picker_instance = query_picker_instance

    def run(self,
            api_address: str,
            url_param: Dict[str, Any],
            active_locations: Dict[str, Any],
            name2id_map: Dict[str, Any]):

        ################################ API DATA FETCHING ################################
        url_builder = self.url_builder_class(api_address=api_address, parameters=url_param)
        url = url_builder.build_url()
        raw_packets = UrllibAdapter.fetch(url)
        parser = self.file_parser_class()
        parsed_packets = parser.parse(raw_packets)

        ################################ RESHAPE PACKETS ################################
        packet_reshaper = self.reshaper_class()
        reshaped_packets = packet_reshaper.reshape_packet(parsed_packets)

        if reshaped_packets:

            ############################## UNIVERSAL ADAPTER #############################
            universal_db_adapter = self.universal_db_adapter_class()

            ############################## ADAPT PACKETS TO THE UNIVERSAL INTERFACE #############################
            universal_packets = []
            for packet in reshaped_packets:
                universal_packets.append(universal_db_adapter.adapt(packet))

            ############################## KEEP ONLY DATABASE SENSORS #############################
            if sc.DEBUG_MODE:
                print(20 * "=" + " FILTER SENSORS " + 20 * '=')
            filtered_universal_packets = []
            for universal_packet in universal_packets:
                if universal_packet['name'] in name2id_map.keys():
                    filtered_universal_packets.append(universal_packet)
                else:
                    print(f"{WARNING_HEADER} '{universal_packet['name']}' => not active")

            ############################## STOP PROGRAM IF NO LOCATION FOUND #############################
            if not filtered_universal_packets:
                print(f"{INFO_HEADER} no active locations found.")
                self.dbconn.close_conn()
                return

            if sc.DEBUG_MODE:
                print(20 * "=" + " ACTIVE SENSORS FOUND " + 20 * '=')
                for universal_packet in filtered_universal_packets:
                    print(f"{DEBUG_HEADER} '{universal_packet['name']}'")

            ############## COMPARE THE OLD LOCATIONS WITH THE NEW DOWNLOADED FROM THE API ###################
            if sc.DEBUG_MODE:
                print(20 * "=" + " UPDATE LOCATIONS " + 20 * '=')

            update_statements = ""
            geo_containers = []
            for universal_packet in filtered_universal_packets:
                name = universal_packet['name']
                geometry = self.postgis_geom_class()
                if geometry.as_text(universal_packet) != active_locations[name]:
                    if sc.DEBUG_MODE:
                        print(f"{INFO_HEADER} '{universal_packet['name']}' => update location")
                    sensor_id = name2id_map[name]
                    # ***************************
                    timestamp = DatetimeParser.current_sqltimestamp()
                    update_statements += self.query_picker_instance.update_valid_to_timestamp_location(sensor_id=sensor_id,
                                                                                                       ts=timestamp)
                    # ***************************
                    geom = geometry.geom_from_text(universal_packet)
                    geo_containers.append(self.geo_sqlcontainer_class(sensor_id=sensor_id, valid_from=timestamp, geom=geom))

            if geo_containers:
                ############################## COMPOSITION CONTAINERS #############################
                geo_container_composition = self.composition_class(geo_containers)

                ############################## BUILD THE QUERY FROM CONTAINERS #############################
                query_statement = self.query_picker_instance.insert_into_sensor_at_location()
                insert_statement = geo_container_composition.sql(query_statement)
                self.dbconn.send(executable_sql_query=update_statements)
                self.dbconn.send(executable_sql_query=insert_statement)
            else:
                print(f"{INFO_HEADER} all sensor have the same location => no location updated.")

        else:
            print(f"{INFO_HEADER} empty packets.")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
