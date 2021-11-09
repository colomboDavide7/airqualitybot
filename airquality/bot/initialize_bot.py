#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 08:30
# @Description: this script contains the classes for initializing the database with different sensor's data.
#
#################################################
from typing import Dict, Any, List

import airquality.constants.system_constants as sc
import airquality.io.remote.api.adapter as api
import airquality.io.remote.database.adapter as db

# IMPORT CLASSES FROM AIRQUALITY MODULE
from utility.query_picker import QueryPicker
from utility.datetime_parser import DatetimeParser
from data.builder.geom import GeometryBuilder
from data.reshaper.uniform.api2db import UniversalDatabaseAdapter
from data.builder.sql import SensorAtLocationSQLBuilder, SQLCompositionBuilder, \
    SensorSQLBuilder, APIParamSQLBuilder

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, INFO_HEADER, WARNING_HEADER


################################ INITIALIZE BOT ################################
class InitializeBot:

    def __init__(self,
                 dbconn: db.DatabaseAdapter,
                 file_parser_class,
                 reshaper_class,
                 query_picker_instance: QueryPicker,
                 url_builder_class,
                 universal_adapter_class=UniversalDatabaseAdapter,
                 geo_sqlcontainer_class=SensorAtLocationSQLBuilder,
                 sensor_sqlcontainer_class=SensorSQLBuilder,
                 apiparam_sqlcontainer_class=APIParamSQLBuilder,
                 composition_class=SQLCompositionBuilder,
                 postgis_geom_class=GeometryBuilder):
        self.dbconn = dbconn
        self.file_parser_class = file_parser_class
        self.url_builder_class = url_builder_class
        self.reshaper_class = reshaper_class
        self.query_picker_instance = query_picker_instance
        self.geo_sqlcontainer_class = geo_sqlcontainer_class
        self.sensor_sqlcontainer_class = sensor_sqlcontainer_class
        self.apiparam_sqlcontainer_class = apiparam_sqlcontainer_class
        self.composition_class = composition_class
        self.universal_db_adapter_class = universal_adapter_class
        self.postgis_geom_class = postgis_geom_class

    def run(self,
            first_sensor_id: int,
            api_address: str,
            url_param: Dict[str, Any],
            sensor_names: List[str]):

        ################################ API DATA FETCHING ################################
        url_builder = self.url_builder_class(api_address=api_address, parameters=url_param)
        url = url_builder.url()
        raw_packets = api.UrllibAdapter.fetch(url)
        parser = self.file_parser_class()
        parsed_packets = parser.parse(raw_packets)

        ################################ RESHAPE PACKETS ################################
        packet_reshaper = self.reshaper_class()
        reshaped_packets = packet_reshaper.reshape_packet(parsed_packets)

        if reshaped_packets:

            ############################## UNIVERSAL ADAPTER #############################
            universal_db_adapter = self.universal_db_adapter_class()

            universal_db_packets = []
            for universal_packet in reshaped_packets:
                universal_db_packets.append(universal_db_adapter.adapt(universal_packet))

            ############################## FILTER PACKETS #############################
            if sc.DEBUG_MODE:
                print(20 * "=" + " FILTER SENSORS " + 20 * '=')
            filtered_universal_packets = []
            for universal_packet in universal_db_packets:
                if universal_packet['name'] not in sensor_names:
                    filtered_universal_packets.append(universal_packet)
                else:
                    print(f"{WARNING_HEADER} '{universal_packet['name']}' => already present")

            if not filtered_universal_packets:
                print(f"{INFO_HEADER} all sensors are already present into the database")
                self.dbconn.close_conn()
                return

            if sc.DEBUG_MODE:
                print(20 * "=" + " NEW SENSORS " + 20 * '=')
                for universal_packet in filtered_universal_packets:
                    print(f"{DEBUG_HEADER} name={universal_packet['name']}")

            ############################## CONVERT PARAMETERS INTO SQL CONTAINERS #############################
            temp_sensor_id = first_sensor_id
            sensor_at_location_values = []
            api_param_values = []
            sensor_values = []
            for universal_packet in filtered_universal_packets:
                # **************************
                sensor_values.append(self.sensor_sqlcontainer_class(sensor_id=temp_sensor_id, packet=universal_packet))
                # **************************
                geometry = self.postgis_geom_class(srid=26918)
                geom = geometry.geom_from_text()
                valid_from = DatetimeParser.current_sqltimestamp()
                sensor_at_location_values.append(self.geo_sqlcontainer_class(sensor_id=temp_sensor_id,
                                                                             valid_from=valid_from,
                                                                             geom=geom))
                # **************************
                api_param_values.append(self.apiparam_sqlcontainer_class(sensor_id=temp_sensor_id, packet=universal_packet))
                temp_sensor_id += 1

            ############################## QUERY HEADERS #############################
            insert_sensor_at_location_header = self.query_picker_instance.insert_into_sensor_at_location()
            insert_api_param_header = self.query_picker_instance.insert_into_api_param()
            insert_sensor_header = self.query_picker_instance.insert_into_sensor()

            ############################## BUILD THE QUERIES FROM VALUES #############################
            query = insert_sensor_header
            for val in sensor_values:
                query += val.sql() + ','
            query = query.strip(',') + ';'
            self.dbconn.send(query)
            # **************************
            query = insert_api_param_header
            for val in api_param_values:
                query += val.sql() + ','
            query = query.strip(',') + ';'
            self.dbconn.send(query)
            # **************************
            query = insert_sensor_at_location_header
            for val in sensor_at_location_values:
                query += val.sql() + ','
            query = query.strip(',') + ';'
            self.dbconn.send(query)
            # **************************
        else:
            print(f"{INFO_HEADER} empty packets.")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
