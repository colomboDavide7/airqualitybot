#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 11:21
# @Description: this script defines the classes for running the update bot
#
#################################################
from typing import Dict, Any

# IMPORT MODULES
import airquality.core.logger.log as log
import airquality.core.logger.decorator as log_decorator
import airquality.io.remote.api.adapter as api
import airquality.io.remote.database.adapter as db
import airquality.data.builder.timest as ts
import airquality.data.builder.url as ub
import airquality.data.builder.sql as sb
import airquality.utility.parser.file as fp
import airquality.utility.picker.query as pk
import airquality.data.reshaper.packet as rshp
import airquality.data.reshaper.uniform.api2db as a2d


################################ UPDATE BOT CLASS ################################
class UpdateBot:

    def __init__(self,
                 dbconn: db.DatabaseAdapter,
                 timestamp: ts.CurrentTimestamp,
                 file_parser: fp.FileParser,
                 query_picker: pk.QueryPicker,
                 url_builder: ub.URLBuilder,
                 packet_reshaper: rshp.PacketReshaper,
                 api2db_uniform_reshaper: a2d.UniformReshaper,
                 geom_builder_class=None,
                 log_filename='update',
                 log_sub_dir='log'):
        self.dbconn = dbconn
        self.timestamp = timestamp
        self.url_builder = url_builder
        self.file_parser = file_parser
        self.query_picker = query_picker
        self.packet_reshaper = packet_reshaper
        self.geom_builder_class = geom_builder_class
        self.a2d_uniform_reshaper = api2db_uniform_reshaper
        self.log_filename = log_filename
        self.log_sub_dir = log_sub_dir
        self.logger = log.get_logger(log_filename=log_filename, log_sub_dir=log_sub_dir)
        self.debugger = log.get_logger(use_color=True)

    ################################ RUN METHOD ################################
    @log_decorator.log_decorator()
    def run(self, database_active_locations: Dict[str, Any], name2id_map: Dict[str, Any]):

        # Build url
        url = self.url_builder.url()
        self.debugger.info(url)
        self.logger.info(url)

        # Fetching data from api
        raw_packets = api.UrllibAdapter.fetch(url)
        parsed_packets = self.file_parser.parse(raw_packets)
        reshaped_packets = self.packet_reshaper.reshape(parsed_packets)

        if not reshaped_packets:
            self.debugger.warning("empty API answer => done")
            self.logger.warning("empty API answer => done")
            self.dbconn.close_conn()
            return

        # Reshape packets such that there is not distinction between packets coming from different sensors
        uniformed_packets = []
        for packet in reshaped_packets:
            uniformed_packets.append(self.a2d_uniform_reshaper.api2db(packet))

        # Filter out all the sensors which name is not in the 'active_locations' keys
        fetched_active_locations = []
        for packet in uniformed_packets:
            if packet['name'] in database_active_locations:
                fetched_active_locations.append(packet)
                self.debugger.info(f"found active location '{packet['name']}'")
                self.logger.info(f"found active location '{packet['name']}'")
            else:
                self.debugger.warning(f"skip location '{packet['name']}' => unknown")
                self.logger.warning(f"skip location '{packet['name']}' => unknown")

        # If no active locations were fetched, stop the program
        if not fetched_active_locations:
            self.debugger.warning("all the locations fetched are unknown => done")
            self.logger.warning("all the locations fetched are unknown => done")
            self.dbconn.close_conn()
            return

        # Update locations
        location_values = []
        for fetched_active_location in fetched_active_locations:
            name = fetched_active_location['name']
            geometry = self.geom_builder_class(fetched_active_location)
            if geometry.as_text() != database_active_locations[name]:
                self.debugger.info(f"found new location={geometry.as_text()} for name='{name}' => update location")
                self.logger.info(f"found new location={geometry.as_text()} for name='{name}' => update location")
                sensor_id = name2id_map[name]
                geom = geometry.geom_from_text()
                value = sb.LocationSQLValueBuilder(sensor_id=sensor_id, valid_from=self.timestamp.ts, geom=geom)
                location_values.append(value)

        if not location_values:
            self.debugger.info("all sensor have the same location => done")
            self.logger.info("all sensor have the same location => done")
            self.dbconn.close_conn()
            return

        ############################## BUILD THE QUERY FROM VALUES #############################
        query = self.query_picker.update_location_values(location_values)
        self.dbconn.send(query)

        self.debugger.info("location(s) successfully updated => done")
        self.logger.info("location(s) successfully updated => done")
        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
