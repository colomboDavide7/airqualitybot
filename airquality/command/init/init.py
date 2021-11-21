######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 11:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Union
import airquality.command.command as c
import airquality.api.fetch as fetch
import airquality.database.operation.insert.init as ins
import airquality.database.operation.select.type as sel_type
import airquality.adapter.api2db.sensor as sens_adapt
import airquality.adapter.api2db.measure as meas_adapt
import airquality.filter.filter as flt
import airquality.logger.util.decorator as log_decorator


class InitCommand(c.Command):

    ################################ __init__ ###############################
    def __init__(self,
                 fetch_wrapper: fetch.FetchWrapper,
                 insert_wrapper: ins.InitializeInsertWrapper,
                 select_type_wrapper: sel_type.TypeSelectWrapper,
                 api2db_adapter: Union[sens_adapt.SensorAdapter, meas_adapt.MeasureAdapter],
                 log_filename="purpleair"
                 ):

        super(InitCommand, self).__init__(
            fetch_wrapper=fetch_wrapper,
            insert_wrapper=insert_wrapper,
            select_type_wrapper=select_type_wrapper,
            api2db_adapter=api2db_adapter,
            log_filename=log_filename
        )

    ################################ execute ###############################
    @log_decorator.log_decorator()
    def execute(self):

        database_sensor_names = self.select_type_wrapper.get_sensor_names()
        if not database_sensor_names:
            self.log_info(f"{InitCommand.__name__}: empty database sensor names")

        # Fetch API data
        sensor_data = self.fetch_wrapper.get_sensor_data()
        if not sensor_data:
            self.log_warning(f"{InitCommand.__name__}: empty API sensor data => no sensor inserted")
            return

        # Reshape API data
        uniformed_sensor_data = [self.api2db_adapter.reshape(d) for d in sensor_data]

        # Create SensorDataFilter
        sensor_data_filter = flt.NameFilter(database_sensor_names=database_sensor_names, log_filename=self.log_filename)
        sensor_data_filter.set_file_logger(self.file_logger)
        sensor_data_filter.set_console_logger(self.console_logger)

        # Filter sensor data
        new_sensor_data = [data for data in uniformed_sensor_data if sensor_data_filter.filter(data)]
        if not new_sensor_data:
            self.log_warning(f"{InitCommand.__name__}: all sensors are already present into the database => no sensor inserted")
            return

        # Query the max 'sensor_id' for knowing the 'sensor_id' during the insertion
        max_sensor_id = self.select_type_wrapper.get_max_sensor_id()

        # Execute queries on sensors
        self.insert_wrapper.insert(sensor_data=new_sensor_data, sensor_id=max_sensor_id)
