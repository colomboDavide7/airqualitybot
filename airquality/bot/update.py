#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 11:21
# @Description: this script defines the classes for running the update bot
#
#################################################
import airquality.bot.base as base


################################ UPDATE BOT CLASS ################################
class UpdateBot(base.BaseBot):

    def __init__(self, log_filename: str, log_sub_dir: str):
        super(UpdateBot, self).__init__(log_filename, log_sub_dir)

    ################################ RUN METHOD ################################
    def execute(self):

        # Query the active locations
        database_active_locations = self.sensor_type_select_wrapper.get_active_locations()
        if not database_active_locations:
            self.warning_messages.append(f"database active locations is empty => no sensor found")
            return

        # Query the (sensor_name, sensor_id) tuples
        name2id_map = self.sensor_type_select_wrapper.get_name_id_map()

        # Fetch API data
        sensor_data = self.fetch_wrapper.get_sensor_data()
        if not sensor_data:
            self.warning_messages.append("no sensor data found => empty API answer")
            return

        # Reshape packets such that there is not distinction between packets coming from different sensors
        uniformed_packets = []
        for data in sensor_data:
            uniformed_packets.append(self.api2db_adapter.reshape(data))

        # Add name to keep external dependency to PacketFilter
        location_names = database_active_locations.keys()
        self.packet_filter.set_name_to_keep(location_names)

        # Apply PacketFilter
        fetched_active_locations = self.packet_filter.filter(uniformed_packets)
        if not fetched_active_locations:
            self.warning_messages.append("all the locations fetched are unknown => done")
            return

        # Update locations
        self.insert_wrapper.update_locations(fetched_locations = fetched_active_locations,
                                             database_locations = database_active_locations,
                                             name2id_map = name2id_map)

        self.info_messages.append("location(s) successfully updated => done")
