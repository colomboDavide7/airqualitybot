#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 08:30
# @Description: this script contains the classes for initializing the database with different sensor's data.
#
#################################################
import airquality.bot.base as base
import airquality.logger.decorator as log_decorator
import airquality.api.fetch as api


################################ INITIALIZE BOT ################################
class InitializeBot(base.BaseBot):

    def __init__(self):
        super(InitializeBot, self).__init__()

    ################################ RUN METHOD ################################
    @log_decorator.log_decorator()
    def run(self):

        # Query database sensor names
        database_sensor_names = self.bot_query_executor.get_sensor_names()

        # Build URL
        url = self.url_builder.url()
        raw_packets = api.fetch(url)
        parsed_packets = self.text_parser_class(raw_packets).parse()
        api_data = self.api_extr_class(parsed_packets).extract()

        if not api_data:
            self.debugger.warning("empty API answer => done")
            self.logger.warning("empty API answer => done")
            return

        # Reshape API data
        uniformed_packets = []
        for fetched_new_sensor in api_data:
            uniformed_packets.append(self.sensor_rshp_class(fetched_new_sensor).reshape())

        # Set external dependency to NameFilter
        self.packet_filter.set_database_sensor_names(database_sensor_names)

        # Apply NameFilter
        fetched_new_sensors = self.packet_filter.filter(uniformed_packets)
        if not fetched_new_sensors:
            self.debugger.info("all sensors are already present into the database => done")
            self.logger.info("all sensors are already present into the database => done")
            return

        # Query the max 'sensor_id' for knowing the 'sensor_id' during the insertion
        starting_new_sensor_id = self.bot_query_executor.get_max_sensor_id()
        msg = f"new insertion starts at sensor_id={starting_new_sensor_id!s}"
        self.debugger.info(msg)
        self.logger.info(msg)

        ############################## BUILD SQL FROM FILTERED UNIFORMED PACKETS #############################
        self.packet_executor.initialize_sensors()

        self.debugger.info("new sensor(s) successfully inserted => done")
        self.logger.info("new sensor(s) successfully inserted => done")
