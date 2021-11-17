#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 11:21
# @Description: this script defines the classes for running the update bot
#
#################################################
import airquality.bot.base as base
import airquality.logger.util.decorator as log_decorator


class UpdateBot(base.BaseBot):

    def __init__(self, log_filename: str, log_sub_dir: str):
        super(UpdateBot, self).__init__(log_filename, log_sub_dir)

    @log_decorator.log_decorator()
    def execute(self):

        # Fetch API data
        sensor_data = self.fetch_wrapper.get_sensor_data()
        if not sensor_data:
            return

        # Reshape packets to a uniform interface
        uniformed_sensor_data = [self.api2db_adapter.reshape(data) for data in sensor_data]

        # Apply GeoFilter to keep only the fetched sensors that have changed location
        fetched_changed_sensors = self.sensor_data_filter.filter(uniformed_sensor_data)
        if not fetched_changed_sensors:
            return

        # Query the (sensor_name, sensor_id) tuples
        name2id_map = self.sensor_type_select_wrapper.get_name_id_map()

        # Update locations
        self.insert_wrapper.update_locations(changed_sensors= fetched_changed_sensors, name2id_map = name2id_map)
