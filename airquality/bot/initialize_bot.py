#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 08:30
# @Description: this script contains the classes for initializing the database with different sensor's data.
#
#################################################
from typing import List

# IMPORT MODULES
import airquality.io.remote.api.adapter as api
import airquality.io.remote.database.adapter as db
import airquality.utility.picker.query as pk
import airquality.data.builder.timest as ts
import airquality.data.builder.url as ub
import airquality.utility.parser.file as fp
import airquality.data.reshaper.packet as rshp
import airquality.data.reshaper.uniform.api2db as a2d
import airquality.data.builder.sql as sb

# IMPORT CONSTANTS
import airquality.core.constants.system_constants as sc
from airquality.core.constants.shared_constants import DEBUG_HEADER, INFO_HEADER, WARNING_HEADER


################################ INITIALIZE BOT ################################
class InitializeBot:

    def __init__(self,
                 dbconn: db.DatabaseAdapter,
                 current_ts: ts.CurrentTimestamp,
                 file_parser: fp.FileParser,
                 packet_reshaper: rshp.PacketReshaper,
                 query_picker: pk.QueryPicker,
                 url_builder: ub.URLBuilder,
                 api2db_uniform_reshaper: a2d.UniformReshaper,
                 sens_at_loc_builder_class=sb.SensorAtLocationSQLBuilder,
                 sensor_builder_class=sb.SensorSQLBuilder,
                 api_param_builder_class=sb.APIParamSQLBuilder,
                 geom_builder_class=None):

        self.dbconn = dbconn
        self.current_ts = current_ts
        self.file_parser = file_parser
        self.packet_reshaper = packet_reshaper
        self.query_picker = query_picker
        self.url_builder = url_builder
        self.a2d_reshaper = api2db_uniform_reshaper
        self.sens_at_loc_builder_class = sens_at_loc_builder_class
        self.sensor_builder_class = sensor_builder_class
        self.api_param_builder_class = api_param_builder_class
        self.geom_builder_class = geom_builder_class

    ################################ RUN METHOD ################################
    def run(self, first_sensor_id: int, sensor_names: List[str]):

        url = self.url_builder.url()                                                # build URL
        raw_packets = api.UrllibAdapter.fetch(url)                                  # fetch data from API
        parsed_packets = self.file_parser.parse(raw_packets)                        # parse API answer
        reshaped_packets = self.packet_reshaper.reshape_packet(parsed_packets)      # reshape API packets

        if not reshaped_packets:
            print(f"{INFO_HEADER} empty API answer")
            self.dbconn.close_conn()
            return

        uniformed_packets = []                                                      # uniformed packets list
        for packet in reshaped_packets:                                             # for each packet...
            uniformed_packets.append(self.a2d_reshaper.api2db(packet))              # ... uniform the packet

        if sc.DEBUG_MODE:
            print(20 * "=" + " FILTER SENSORS " + 20 * '=')

        filtered_packets = []                                                       # filtered packets list
        for uniformed_packet in uniformed_packets:                                  # for each packet...
            if uniformed_packet['name'] not in sensor_names:                        # ...if is not presents into DB...
                filtered_packets.append(uniformed_packet)                           # ...add to the list
            else:
                print(f"{WARNING_HEADER} '{uniformed_packet['name']}' => already present")

        if not filtered_packets:
            print(f"{INFO_HEADER} all sensors are already present into the database")
            self.dbconn.close_conn()
            return

        if sc.DEBUG_MODE:
            print(20 * "=" + " NEW SENSORS " + 20 * '=')
            for packet in filtered_packets:
                print(f"{DEBUG_HEADER} name='{packet['name']}'")

        ############################## BUILD SQL FROM FILTERED UNIFORMED PACKETS #############################
        tmp_id = first_sensor_id
        sensor_at_location_values = []
        api_param_values = []
        sensor_values = []
        for packet in filtered_packets:
            # **************************
            sensor_value = self.sensor_builder_class(sensor_id=tmp_id, packet=packet)
            sensor_values.append(sensor_value)
            # **************************
            geometry = self.geom_builder_class(srid=26918, packet=packet)
            valid_from = self.current_ts.ts
            geom = geometry.geom_from_text()
            geom_value = self.sens_at_loc_builder_class(sensor_id=tmp_id, valid_from=valid_from, geom=geom)
            sensor_at_location_values.append(geom_value)
            # **************************
            api_param_value = self.api_param_builder_class(sensor_id=tmp_id, packet=packet)
            api_param_values.append(api_param_value)
            # **************************
            tmp_id += 1

        ################################ BUILD + EXECUTE QUERIES ################################
        query = self.query_picker.insert_into_sensor(sensor_values)
        query += self.query_picker.insert_into_api_param(api_param_values)
        query += self.query_picker.insert_into_sensor_at_location(sensor_at_location_values)
        self.dbconn.send(query)

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
