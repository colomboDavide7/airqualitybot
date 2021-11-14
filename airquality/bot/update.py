#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 11:21
# @Description: this script defines the classes for running the update bot
#
#################################################
import airquality.bot.base as base
import airquality.logger.decorator as log_decorator
import airquality.api.fetch as api


################################ UPDATE BOT CLASS ################################
class UpdateBot(base.BaseBot):

    def __init__(self):
        super(UpdateBot, self).__init__()

    ################################ RUN METHOD ################################
    @log_decorator.log_decorator()
    def run(self):

        # Query the active locations
        database_active_locations = self.bot_query_executor.get_active_locations()
        if not database_active_locations:
            self.debugger.warning(f"no sensor found => done")
            self.logger.warning(f"no sensor found => done")
            return

        # Query the (sensor_name, sensor_id) tuples
        name2id_map = self.bot_query_executor.get_name_id_map()

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
        self.insertion_executor.update_locations(fetched_locations = fetched_active_locations,
                                                 database_locations = database_active_locations,
                                                 name2id_map = name2id_map)

        self.debugger.info("location(s) successfully updated => done")
        self.logger.info("location(s) successfully updated => done")
