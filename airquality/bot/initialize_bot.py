#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 08:30
# @Description: this script contains the classes for initializing the database with different sensor's data.
#
#################################################
from typing import List

# IMPORT MODULES
import logging
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

################################ INITIALIZE LOGGER ################################
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename='log/initialize.log', mode='a')
formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


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
                 geom_builder_class=None):

        self.dbconn = dbconn
        self.timestamp = timestamp
        self.file_parser = file_parser
        self.packet_reshaper = packet_reshaper
        self.query_picker = query_picker
        self.url_builder = url_builder
        self.a2d_reshaper = api2db_uniform_reshaper
        self.geom_builder_class = geom_builder_class

    ################################ RUN METHOD ################################
    def run(self, first_sensor_id: int, sensor_names: List[str]):

        url = self.url_builder.url()
        raw_packets = api.UrllibAdapter.fetch(url)
        parsed_packets = self.file_parser.parse(raw_packets)
        reshaped_packets = self.packet_reshaper.reshape(parsed_packets)

        if not reshaped_packets:
            msg = "empty API answer"
            print(f"{INFO_HEADER} {msg}")
            logger.info(msg)
            self.dbconn.close_conn()
            return

        uniformed_packets = []
        for packet in reshaped_packets:
            uniformed_packets.append(self.a2d_reshaper.api2db(packet))

        print(20 * "=" + " FILTER FETCHED SENSORS " + 20 * '=')
        filtered_packets = []
        for uniformed_packet in uniformed_packets:
            if uniformed_packet['name'] not in sensor_names:
                filtered_packets.append(uniformed_packet)
            else:
                print(f"{WARNING_HEADER} '{uniformed_packet['name']}' => already present")

        if not filtered_packets:
            msg = "all sensors are already present into the database => done"
            print(f"{INFO_HEADER} {msg}")
            logger.info(msg)
            self.dbconn.close_conn()
            return

        print(20 * "=" + " NEW SENSORS FETCHED " + 20 * '=')
        if sc.DEBUG_MODE:
            for packet in filtered_packets:
                print(f"{DEBUG_HEADER} name='{packet['name']}'")

        ############################## BUILD SQL FROM FILTERED UNIFORMED PACKETS #############################
        tmp_id = first_sensor_id
        location_values = []
        api_param_values = []
        sensor_values = []
        for packet in filtered_packets:
            # **************************
            sensor_value = sb.SensorSQLValueBuilder(sensor_id=tmp_id, packet=packet)
            sensor_values.append(sensor_value)
            # **************************
            geometry = self.geom_builder_class(packet)
            valid_from = self.timestamp.ts
            geom = geometry.geom_from_text()
            geom_value = sb.LocationSQLValueBuilder(sensor_id=tmp_id, valid_from=valid_from, geom=geom)
            location_values.append(geom_value)
            # **************************
            api_param_value = sb.APIParamSQLValueBuilder(sensor_id=tmp_id, packet=packet)
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
        logger.info("new sensor(s) successfully inserted => done")
        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
