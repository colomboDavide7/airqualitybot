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
from airquality.api.url_builder import URLBuilder
from airquality.api.urllib_adapter import UrllibAdapter
from airquality.geom.postgis_geometry import PostGISGeometry
from airquality.parser.datetime_parser import DatetimeParser
from airquality.reshaper.packet_reshaper import PacketReshaper
from airquality.adapter.universal_db_adapter import UniversalDatabaseAdapter
from airquality.container.sql_container import GeoSQLContainer, SQLContainerComposition

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, INFO_HEADER, WARNING_HEADER


################################ GEO BOT ABSTRACT BASE CLASS ################################
class GeoBot:

    def __init__(self,
                 dbconn,
                 file_parser_class,
                 url_builder_class=URLBuilder,
                 reshaper_class=PacketReshaper,
                 universal_db_adapter_class=UniversalDatabaseAdapter,
                 geom_sqlcontainer_class=GeoSQLContainer,
                 composition_class=SQLContainerComposition,
                 postgis_geom_class=PostGISGeometry):
        self.dbconn = dbconn
        self.url_builder_class = url_builder_class
        self.file_parser_class = file_parser_class
        self.reshaper_class = reshaper_class
        self.universal_db_adapter_class = universal_db_adapter_class
        self.geo_sqlcontainer_class = geom_sqlcontainer_class
        self.composition_class = composition_class
        self.postgis_geom_class = postgis_geom_class

    def run(self,
            api_address: str,
            url_param: Dict[str, Any],
            active_locations: Dict[str, Any],
            name2id_map: Dict[str, Any],
            update_valid_to_ts_query: str,
            sensor_at_location_query: str):

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
                    print(f"{DEBUG_HEADER} name={universal_packet['name']}")

            ############## COMPARE THE OLD LOCATIONS WITH THE NEW DOWNLOADED FROM THE API ###################
            update_statements = ""
            geo_containers = []
            for universal_packet in filtered_universal_packets:
                name = universal_packet['name']
                geometry = self.postgis_geom_class()
                if geometry.get_geomtype_string(universal_packet) != active_locations[name]:
                    sensor_id = name2id_map[name]
                    # ***************************
                    timestamp = DatetimeParser.current_sqltimestamp()
                    update_statements += update_valid_to_ts_query.format(sens_id=sensor_id,
                                                                         ts=timestamp)
                    # ***************************
                    geom = geometry.get_database_string(universal_packet)
                    geo_containers.append(self.geo_sqlcontainer_class(sensor_id=sensor_id,
                                                                      valid_from=timestamp,
                                                                      geom=geom))

            if geo_containers:
                ############################## COMPOSITION CONTAINERS #############################
                geo_container_composition = self.composition_class(geo_containers)

                ############################## BUILD THE QUERY FROM CONTAINERS #############################
                insert_statement = geo_container_composition.sql(query=sensor_at_location_query)
                self.dbconn.send(executable_sql_query=update_statements)
                self.dbconn.send(executable_sql_query=insert_statement)
            else:
                print(f"{INFO_HEADER} all sensor have the same location => no location updated.")

        else:
            print(f"{INFO_HEADER} empty packets.")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
