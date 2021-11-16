#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 11:21
# @Description: this script defines the classes for running the update bot
#
#################################################
import airquality.bot.base as base
import airquality.filter.filter as filt


################################ UPDATE BOT CLASS ################################
class UpdateBot(base.BaseBot):

    def __init__(self, log_filename: str, log_sub_dir: str):
        super(UpdateBot, self).__init__(log_filename, log_sub_dir)
        self.geo_filter = None

    def add_geo_filter(self, filter_obj: filt.GeoFilter):
        self.geo_filter = filter_obj

    ################################ RUN METHOD ################################
    def execute(self):

        if self.geo_filter is None:
            raise SystemExit(f"{UpdateBot.__name__}: bad setup => missing external dependency 'geo_filter'")

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

        # Reshape packets to a uniform interface
        uniformed_packets = []
        for data in sensor_data:
            uniformed_packets.append(self.api2db_adapter.reshape(data))

        # Add external dependency to NameFilter
        location_names = database_active_locations.keys()
        self.sensor_data_filter.set_name_to_keep(location_names)

        # Apply NameFilter to filter out all the fetched sensors that are not active
        fetched_active_sensors = self.sensor_data_filter.filter(uniformed_packets)
        if not fetched_active_sensors:
            self.warning_messages.append("all the locations fetched are unknown => done")
            return

        # Inject external dependencies to GeoFilter
        self.geo_filter.set_database_active_locations(database_active_locations)

        # Apply GeoFilter to keep only the fetched sensors that have changed location
        fetched_changed_sensors = self.geo_filter.filter(fetched_active_sensors)
        if not fetched_changed_sensors:
            self.info_messages.append("all the sensors have the same location => done")
            return

        # Update locations
        self.insert_wrapper.update_locations(changed_sensors= fetched_changed_sensors, name2id_map = name2id_map)

        self.info_messages.append("location(s) successfully updated => done")
