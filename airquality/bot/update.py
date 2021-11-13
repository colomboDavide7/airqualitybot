#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 11:21
# @Description: this script defines the classes for running the update bot
#
#################################################
import airquality.bot.base as base
import airquality.core.logger.decorator as log_decorator
import airquality.stream.remote.api.adapter as api
import airquality.stream.remote.database.adapter as db
import airquality.data.builder.sql as sb


################################ UPDATE BOT CLASS ################################
class UpdateBot(base.BaseBot):

    def __init__(self, sensor_type: str, dbconn: db.DatabaseAdapter):
        super(UpdateBot, self).__init__(sensor_type=sensor_type, dbconn=dbconn)

    @log_decorator.log_decorator()
    def run(self):

        # Query the active locations
        query = self.query_picker.select_active_locations(self.sensor_type)
        answer = self.dbconn.send(query)
        database_active_locations = dict(answer)

        if not database_active_locations:
            self.debugger.warning(f"no sensor found for type='{self.sensor_type}' => done")
            self.logger.warning(f"no sensor found for type='{self.sensor_type}' => done")
            return

        # Query the (sensor_name, sensor_id) tuples
        query = self.query_picker.select_sensor_name_id_mapping_from_sensor_type(self.sensor_type)
        answer = self.dbconn.send(query)
        name2id_map = dict(answer)

        # Fetch API data
        url = self.url_builder.url()
        raw_packets = api.fetch(url)
        parsed_packets = self.text_parser_class(raw_packets).parse()
        api_data = self.api_extr_class(parsed_packets).extract()

        if not api_data:
            self.debugger.warning("empty API answer => done")
            self.logger.warning("empty API answer => done")
            return

        # Reshape packets such that there is not distinction between packets coming from different sensors
        uniformed_packets = []
        for sensor_data in api_data:
            uniformed_packets.append(self.sensor_rshp_class(sensor_data).reshape())

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
                value = sb.LocationSQLValueBuilder(sensor_id=sensor_id, valid_from=self.current_ts.ts, geom=geom)
                location_values.append(value)

        if not location_values:
            self.debugger.info("all sensor have the same location => done")
            self.logger.info("all sensor have the same location => done")
            return

        ############################## BUILD THE QUERY FROM VALUES #############################
        query = self.query_picker.update_location_values(location_values)
        self.dbconn.send(query)

        self.debugger.info("location(s) successfully updated => done")
        self.logger.info("location(s) successfully updated => done")
