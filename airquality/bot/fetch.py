#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 11:33
# @Description: this script defines the bot classes for the fetch module
#
#################################################
from typing import Dict, Any
import airquality.bot.base as base
import airquality.database.util.datatype.timestamp as ts
import airquality.database.operation.select.type as select
import airquality.adapter.config as adapt_const
import airquality.logger.util.decorator as log_decorator
import airquality.bot.util.datelooper as loop


################################ FETCH BOT ################################
class FetchBot(base.BaseBot):

    def __init__(self, log_filename="app"):
        super(FetchBot, self).__init__(log_filename=log_filename)
        self.date_looper_class = None
        self.sensor_id_select_wrapper = None

    def add_date_looper_class(self, looper_class=loop.DateLooper):
        self.date_looper_class = looper_class

    def add_sensor_id_select_wrapper(self, wrapper: select.SensorIDSelectWrapper):
        self.sensor_id_select_wrapper = wrapper

    def _exit_on_missing_external_dependencies(self):
        if self.sensor_id_select_wrapper is None:
            raise SystemExit(f"{FetchBot.__name__}: bad setup => missing external dependency 'sensor_id_select_wrapper'")
        if self.date_looper_class is None:
            raise SystemExit(f"{FetchBot.__name__}: bad setup => missing external dependency 'date_looper_class'")

################################ FUNCTION 0 ################################
    @log_decorator.log_decorator()
    def execute(self):

        self._exit_on_missing_external_dependencies()

        # Query sensor ids from database
        database_sensor_ids = self.sensor_type_select_wrapper.get_sensor_id()
        if not database_sensor_ids:
            self.log_warning(f"{FetchBot.__name__}: no sensor found inside the database => no measure inserted")
            return

        # Fetch new measure for each database sensor id
        for sensor_id in database_sensor_ids:
            self._fetch_measurements_from_sensor_id(sensor_id=sensor_id)

############################# FUNCTION 1 ##############################
    @log_decorator.log_decorator()
    def _fetch_measurements_from_sensor_id(self, sensor_id: int):

        # Extract database API parameters
        database_api_param = self.sensor_id_select_wrapper.get_sensor_api_param(sensor_id=sensor_id)

        # Get a List of the API parameters for each channel of the sensor
        channel_api_param = self.db2api_adapter.reshape(database_api_param=database_api_param)

        # Cycle on one channel at a time
        for api_param in channel_api_param:
            self._fetch_measurements_from_sensor_channel(sensor_id=sensor_id, api_param=api_param)

############################# FUNCTION 2 ##############################
    @log_decorator.log_decorator()
    def _fetch_measurements_from_sensor_channel(self, sensor_id: int, api_param: Dict[str, Any]):

        # Pop channel name
        channel_name = api_param.pop(adapt_const.CH_NAME)

        # Query sensor channel last acquisition
        last_acquisition = self.sensor_id_select_wrapper.get_last_acquisition(channel=channel_name, sensor_id=sensor_id)
        filter_timestamp = ts.SQLTimestamp(last_acquisition)
        self.log_info(f"{FetchBot.__name__}: last acquisition => {filter_timestamp.get_formatted_timestamp()}")

        # Set 'filter_ts' dependency
        self.sensor_data_filter.set_filter_ts(filter_ts=filter_timestamp)

        # DateLooper
        looper = self.date_looper_class(fetch_wrapper=self.fetch_wrapper, start_ts=filter_timestamp, stop_ts=ts.CurrentTimestamp(),
                                        log_filename=self.log_filename)
        looper.set_file_logger(self.file_logger)
        looper.set_console_logger(self.console_logger)

        # Update parameters and set channel name
        looper.update_url_param(api_param)
        looper.set_channel_name(channel_name)

        # Fetch data within a given time period
        while looper.has_next():
            sensor_data = looper.get_next_sensor_data()
            if not sensor_data:
                self.log_warning(f"{FetchBot.__name__}: empty API sensor data => continue")
                continue

            # Filter and insert measurements
            self._uniform_filter_insert(sensor_id=sensor_id, channel_name=channel_name, sensor_data=sensor_data)

############################# FUNCTION 3 ##############################
    @log_decorator.log_decorator()
    def _uniform_filter_insert(self, sensor_id: int, channel_name: str, sensor_data: Dict[str, Any]):

        # Uniform sensor data
        uniformed_sensor_data = [self.api2db_adapter.reshape(data) for data in sensor_data]

        # Filter measure to keep only new measurements
        new_data = [data for data in uniformed_sensor_data if self.sensor_data_filter.filter(data)]

        # Log message
        self.log_info(f"{FetchBot.__name__}: found {len(new_data)}/{len(uniformed_sensor_data)} new measurements")
        if not new_data:
            return

        # Insert measurements
        self.insert_wrapper.insert_measurements(sensor_data=new_data, sensor_id=sensor_id, channel=channel_name)
