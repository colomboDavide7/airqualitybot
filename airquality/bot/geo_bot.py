#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 11:21
# @Description: this script defines the classes for running the geo bot
#
#################################################
from typing import Dict, Any

# IMPORT MODULES
import airquality.io.remote.api.adapter as api
import airquality.io.remote.database.adapter as db
import airquality.data.builder.timest as ts
import airquality.data.builder.url as ub
import airquality.data.builder.sql as sb
import airquality.utility.parser.file as fp
import airquality.utility.picker.query as pk
import airquality.data.reshaper.packet as rshp
import airquality.data.reshaper.uniform.api2db as a2d

# IMPORT CONSTANTS
import airquality.core.constants.system_constants as sc
from airquality.core.constants.shared_constants import DEBUG_HEADER, INFO_HEADER, WARNING_HEADER


################################ GEO BOT CLASS ################################
class GeoBot:

    def __init__(self,
                 dbconn: db.DatabaseAdapter,
                 current_ts: ts.CurrentTimestamp,
                 file_parser: fp.FileParser,
                 query_picker: pk.QueryPicker,
                 url_builder: ub.URLBuilder,
                 packet_reshaper: rshp.PacketReshaper,
                 api2db_uniform_reshaper: a2d.UniformReshaper,
                 sens_at_loc_builder_class=sb.SensorAtLocationSQLBuilder,
                 geom_builder_class=None):
        self.dbconn = dbconn
        self.current_ts = current_ts
        self.url_builder = url_builder
        self.file_parser = file_parser
        self.query_picker = query_picker
        self.packet_reshaper = packet_reshaper
        self.geom_builder_class = geom_builder_class
        self.a2d_uniform_reshaper = api2db_uniform_reshaper
        self.sens_at_loc_builder_class = sens_at_loc_builder_class

    ################################ RUN METHOD ################################
    def run(self, active_locations: Dict[str, Any], name2id_map: Dict[str, Any]):

        url = self.url_builder.url()
        raw_packets = api.UrllibAdapter.fetch(url)
        parsed_packets = self.file_parser.parse(raw_packets)
        reshaped_packets = self.packet_reshaper.reshape(parsed_packets)

        if not reshaped_packets:
            print(f"{INFO_HEADER} empty API answer")
            self.dbconn.close_conn()
            return

        uniformed_packets = []
        for packet in reshaped_packets:
            uniformed_packets.append(self.a2d_uniform_reshaper.api2db(packet))

        if sc.DEBUG_MODE:
            print(20 * "=" + " FILTER FETCHED SENSORS " + 20 * '=')
        filtered_packets = []
        for uniformed_packet in uniformed_packets:
            if uniformed_packet['name'] in name2id_map.keys():
                filtered_packets.append(uniformed_packet)
            else:
                print(f"{WARNING_HEADER} '{uniformed_packet['name']}' => not active")

        if not filtered_packets:
            print(f"{INFO_HEADER} no active locations found.")
            self.dbconn.close_conn()
            return

        if sc.DEBUG_MODE:
            print(20 * "=" + " FETCHED ACTIVE SENSORS " + 20 * '=')
            for packet in filtered_packets:
                print(f"{DEBUG_HEADER} '{packet['name']}'")

        ############## COMPARE THE OLD LOCATIONS WITH THE NEW DOWNLOADED FROM THE API ###################
        if sc.DEBUG_MODE:
            print(20 * "=" + " UPDATE LOCATIONS " + 20 * '=')

        update = ""
        sens_at_loc_values = []
        for packet in filtered_packets:
            name = packet['name']
            geometry = self.geom_builder_class(srid=26918, packet=packet)
            if geometry.as_text() != active_locations[name]:
                if sc.DEBUG_MODE:
                    print(f"{INFO_HEADER} '{name}' => update location")
                # ***************************
                sensor_id = name2id_map[name]
                update += self.query_picker.update_valid_to_location_timestamp(sensor_id=sensor_id, ts=self.current_ts.ts)
                # ***************************
                geom = geometry.geom_from_text()
                value = self.sens_at_loc_builder_class(sensor_id=sensor_id, valid_from=self.current_ts.ts, geom=geom)
                sens_at_loc_values.append(value)

        if not sens_at_loc_values:
            print(f"{INFO_HEADER} all sensor have the same location => no location updated.")
            self.dbconn.close_conn()
            return

        ############################## BUILD THE QUERY FROM CONTAINERS #############################
        insert = self.query_picker.insert_into_sensor_at_location(sens_at_loc_values)
        self.dbconn.send(update)
        self.dbconn.send(insert)

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
