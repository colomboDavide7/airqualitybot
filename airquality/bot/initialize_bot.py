#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 08:30
# @Description: this script contains the classes for initializing the database with different sensor's data.
#
#################################################
from typing import List

# IMPORT MODULES
import airquality.core.logger.log as log
import airquality.core.logger.decorator as log_decorator
import airquality.io.remote.api.adapter as api
import airquality.io.remote.database.adapter as db
import airquality.utility.picker.query as pk
import airquality.data.builder.timest as ts
import airquality.data.builder.url as ub
import airquality.utility.parser.file as fp
import airquality.data.reshaper.packet as rshp
import airquality.data.reshaper.uniform.api2db as a2d
import airquality.data.builder.sql as sb


################################ INITIALIZE BOT ################################
class InitializeBot:

    def __init__(self,
                 dbconn: db.DatabaseAdapter,
                 timestamp: ts.CurrentTimestamp,
                 file_parser: fp.FileParser,
                 packet_reshaper: rshp.PacketReshaper,
                 query_picker: pk.QueryPicker,
                 url_builder: ub.URLBuilder,
                 api2db_uniform_reshaper: a2d.UniformReshaper,
                 geom_builder_class=None,
                 log_filename='initialize',
                 log_sub_dir='log'):

        self.dbconn = dbconn
        self.timestamp = timestamp
        self.file_parser = file_parser
        self.packet_reshaper = packet_reshaper
        self.query_picker = query_picker
        self.url_builder = url_builder
        self.a2d_reshaper = api2db_uniform_reshaper
        self.geom_builder_class = geom_builder_class
        self.log_filename = log_filename
        self.log_sub_dir = log_sub_dir
        self.logger = log.get_logger(log_filename=log_filename, log_sub_dir=log_sub_dir)
        self.debugger = log.get_logger(use_color=True)

    ################################ RUN METHOD ################################
    @log_decorator.log_decorator()
    def run(self, first_sensor_id: int, database_sensor_names: List[str]):

        url = self.url_builder.url()
        raw_packets = api.UrllibAdapter.fetch(url)
        parsed_packets = self.file_parser.parse(raw_packets)
        reshaped_packets = self.packet_reshaper.reshape(parsed_packets)

        if not reshaped_packets:
            self.debugger.warning("empty API answer => done")
            self.logger.warning("empty API answer => done")
            self.dbconn.close_conn()
            return

        uniformed_packets = []
        for fetched_new_sensor in reshaped_packets:
            uniformed_packets.append(self.a2d_reshaper.api2db(fetched_new_sensor))

        # Remove fetched sensors that are already present into the database
        fetched_new_sensors = []
        for uniformed_packet in uniformed_packets:
            if uniformed_packet['name'] not in database_sensor_names:
                fetched_new_sensors.append(uniformed_packet)
                self.debugger.info(f"found new sensor '{uniformed_packet['name']}'")
                self.logger.info(f"found new sensor '{uniformed_packet['name']}'")
            else:
                self.debugger.warning(f"skip sensor '{uniformed_packet['name']}' => already present")
                self.logger.warning(f"skip sensor '{uniformed_packet['name']}' => already present")

        if not fetched_new_sensors:
            self.debugger.info("all sensors are already present into the database => done")
            self.logger.info("all sensors are already present into the database => done")
            self.dbconn.close_conn()
            return

        ############################## BUILD SQL FROM FILTERED UNIFORMED PACKETS #############################
        tmp_id = first_sensor_id
        location_values = []
        api_param_values = []
        sensor_values = []
        for fetched_new_sensor in fetched_new_sensors:
            # **************************
            sensor_value = sb.SensorSQLValueBuilder(sensor_id=tmp_id, packet=fetched_new_sensor)
            sensor_values.append(sensor_value)
            # **************************
            geometry = self.geom_builder_class(fetched_new_sensor)
            valid_from = self.timestamp.ts
            geom = geometry.geom_from_text()
            geom_value = sb.LocationSQLValueBuilder(sensor_id=tmp_id, valid_from=valid_from, geom=geom)
            location_values.append(geom_value)
            # **************************
            api_param_value = sb.APIParamSQLValueBuilder(sensor_id=tmp_id, packet=fetched_new_sensor)
            api_param_values.append(api_param_value)
            # **************************
            tmp_id += 1

        ################################ BUILD + EXECUTE QUERIES ################################
        query = self.query_picker.initialize_sensors(
            sensor_values=sensor_values,
            api_param_values=api_param_values,
            location_values=location_values
        )
        self.dbconn.send(query)

        self.debugger.info("new sensor(s) successfully inserted => done")
        self.logger.info("new sensor(s) successfully inserted => done")
        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
