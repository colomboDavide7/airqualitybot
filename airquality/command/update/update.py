######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Union
import airquality.logger.util.decorator as log_decorator
import airquality.command.command as base
import airquality.api.fetch as fetch
import airquality.database.operation.insert.update as ins
import airquality.database.operation.select.type as sel_type
import airquality.adapter.api2db.sensor as sens_adapt
import airquality.adapter.api2db.measure as meas_adapt
import airquality.filter.filter as flt


class UpdateCommand(base.Command):

    ################################ __init__ ################################
    def __init__(self,
                 fetch_wrapper: fetch.FetchWrapper,
                 insert_wrapper: ins.UpdateInsertWrapper,
                 select_type_wrapper: sel_type.TypeSelectWrapper,
                 api2db_adapter: Union[sens_adapt.SensorAdapter, meas_adapt.MeasureAdapter],
                 log_filename="purpleair"
                 ):

        super(UpdateCommand, self).__init__(
            fetch_wrapper=fetch_wrapper,
            insert_wrapper=insert_wrapper,
            select_type_wrapper=select_type_wrapper,
            api2db_adapter=api2db_adapter,
            log_filename=log_filename)

    ################################ execute ################################
    @log_decorator.log_decorator()
    def execute(self):

        # Query database active locations
        database_active_locations = self.select_type_wrapper.get_active_locations()
        if not database_active_locations:
            self.log_warning(f"{UpdateCommand.__name__}: empty database active locations => no location updated")
            return

        # Fetch API data
        sensor_data = self.fetch_wrapper.get_sensor_data()
        if not sensor_data:
            self.log_warning(f"{UpdateCommand.__name__}: empty API sensor data => no location updated")
            return

        # Reshape packets to a uniform interface
        uniformed_sensor_data = [self.api2db_adapter.reshape(data) for data in sensor_data]

        # Create GeoFilter
        sensor_data_filter = flt.GeoFilter(database_active_locations=database_active_locations, log_filename=self.log_filename)
        sensor_data_filter.set_file_logger(self.file_logger)
        sensor_data_filter.set_console_logger(self.console_logger)

        # Filter sensor data
        fetched_changed_sensors = [data for data in uniformed_sensor_data if sensor_data_filter.filter(data)]
        if not fetched_changed_sensors:
            self.log_warning(f"{UpdateCommand.__name__}: all sensor locations are the same => no location updated")
            return

        # Query the (sensor_name, sensor_id) tuples
        name2id_map = self.select_type_wrapper.get_name_id_map()

        # Inject external dependency to InsertWrapper
        self.insert_wrapper.set_name_to_id_map(name2id_map)

        # Update locations
        self.insert_wrapper.insert(sensor_data=fetched_changed_sensors)
