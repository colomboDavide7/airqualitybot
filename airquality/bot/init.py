#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 08:30
# @Description: this script contains the classes for initializing the database with different sensor's data.
#
#################################################
import airquality.bot.base as base
import airquality.logger.util.decorator as log_decorator


class InitializeBot(base.BaseBot):

    def __init__(self, log_filename="app"):
        super(InitializeBot, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def execute(self):

        # Fetch API data
        sensor_data = self.fetch_wrapper.get_sensor_data()
        if not sensor_data:
            self.log_warning(f"{InitializeBot.__name__}: empty API sensor data => no sensor inserted")
            return

        # Reshape API data
        uniformed_sensor_data = [self.api2db_adapter.reshape(d) for d in sensor_data]

        # Apply SensorDataFilter to keep only new sensors
        new_sensor_data = [data for data in uniformed_sensor_data if self.sensor_data_filter.filter(data)]
        if not new_sensor_data:
            self.log_warning(f"{InitializeBot.__name__}: all the sensors are already present into the database "
                             f"=> no sensor inserted")
            return

        # Query the max 'sensor_id' for knowing the 'sensor_id' during the insertion
        max_sensor_id = self.sensor_type_select_wrapper.get_max_sensor_id()
        # Execute queries on sensors
        self.insert_wrapper.initialize_sensors(sensor_data=new_sensor_data, start_id=max_sensor_id)
