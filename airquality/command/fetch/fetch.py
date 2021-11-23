######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 17:49
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Union, Dict, Any, List
import airquality.api.fetchwrp as fetch
import airquality.command.command as base
import airquality.adapter.config as adapt_const
import airquality.logger.util.decorator as log_decorator
import airquality.database.operation.insert.insert as ins
import airquality.database.operation.select.sensor as sel_type
import container.sensor as sens_adapt
import airquality.adapter.api2db.measure as meas_adapt
import airquality.adapter.db2api.param as par_adapt
import airquality.database.util.datatype.timestamp as ts
import airquality.filter.filter as flt


class FetchCommand(base.Command):

    ################################ __init__ ###############################
    def __init__(self,
                 fetch_wrapper: fetch.FetchWrapper,
                 insert_wrapper: ins.InsertWrapper,
                 select_type_wrapper: sel_type.TypeSelectWrapper,
                 id_select_wrapper: sel_type.SensorIDSelectWrapper,
                 api2db_adapter: Union[sens_adapt.SensorContainerBuilder, meas_adapt.MeasureAdapter],
                 db2api_adapter: par_adapt.ParamAdapter,
                 date_looper_class,
                 log_filename="log"
                 ):
        super(FetchCommand, self).__init__(
            fetch_wrapper=fetch_wrapper,
            insert_wrapper=insert_wrapper,
            select_type_wrapper=select_type_wrapper,
            api2db_adapter=api2db_adapter,
            log_filename=log_filename)
        self.db2api_adapter = db2api_adapter
        self.id_select_wrapper = id_select_wrapper
        self.date_looper_class = date_looper_class

    ################################ execute ###############################
    @log_decorator.log_decorator()
    def execute(self):

        # Query sensor ids from database
        database_sensor_ids = self.select_type_wrapper.get_sensor_id()
        if not database_sensor_ids:
            self.log_warning(f"{FetchCommand.__name__}: no sensor found inside the database => no measure inserted")
            return

        # Fetch new measure for each database sensor id
        for sensor_id in database_sensor_ids:
            self._fetch_measurements_from_sensor_id(sensor_id=sensor_id)

    ############################# FUNCTION 1 ##############################
    @log_decorator.log_decorator()
    def _fetch_measurements_from_sensor_id(self, sensor_id: int):

        # Extract database API parameters
        database_api_param = self.id_select_wrapper.get_sensor_api_param(sensor_id=sensor_id)

        # Get a List of the API parameters for each channel of the sensor
        channel_api_param = self.db2api_adapter.reshape(database_api_param=database_api_param)

        # Cycle on one channel at a time
        for api_param in channel_api_param:
            self._fetch_sensor_channel_measurements(sensor_id=sensor_id, api_param=api_param)

    ############################# FUNCTION 2 ##############################
    @log_decorator.log_decorator()
    def _fetch_sensor_channel_measurements(self, sensor_id: int, api_param: Dict[str, Any]):

        # Pop channel name
        channel_name = api_param.pop(adapt_const.CH_NAME)

        # Query sensor channel last acquisition
        last_acquisition = self.id_select_wrapper.get_last_acquisition(channel=channel_name, sensor_id=sensor_id)
        filter_timestamp = ts.SQLTimestamp(last_acquisition)
        self.log_info(f"{FetchCommand.__name__}: last acquisition => {filter_timestamp.get_formatted_timestamp()}")

        # Create TimestampFilter to keep only new measurements and remove the old ones
        sensor_data_filter = flt.TimestampFilter(log_filename=self.log_filename)
        sensor_data_filter.set_filter_ts(filter_ts=filter_timestamp)

        # DateLooper
        looper = self.date_looper_class(fetch_wrapper=self.fetch_wrapper,
                                        start_ts=filter_timestamp,
                                        stop_ts=ts.CurrentTimestamp(),
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
                self.log_warning(f"{FetchCommand.__name__}: empty API sensor data => continue")
                continue

            # Filter and insert measurements
            self._uniform_filter_insert(
                sensor_data_flt=sensor_data_filter,
                sensor_id=sensor_id,
                channel_name=channel_name,
                sensor_data=sensor_data
            )

    ############################# FUNCTION 3 ##############################
    @log_decorator.log_decorator()
    def _uniform_filter_insert(self,
                               sensor_data_flt: flt.SensorDataFilter,
                               sensor_id: int,
                               channel_name: str,
                               sensor_data: List[Dict[str, Any]]
    ):

        # Uniform sensor data
        uniformed_sensor_data = [self.api2db_adapter.raw2container(data) for data in sensor_data]

        # Filter measure to keep only new measurements
        new_data = [data for data in uniformed_sensor_data if sensor_data_flt.filter(data)]

        # Log message
        self.log_info(f"{FetchCommand.__name__}: found {len(new_data)}/{len(uniformed_sensor_data)} new measurements")
        if not new_data:
            return

        # Insert measurements
        self.insert_wrapper.insert(sensor_data=new_data, sensor_id=sensor_id, sensor_channel=channel_name)
