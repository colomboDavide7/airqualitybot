######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 11:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Union
import airquality.command.command as c
import airquality.api.fetchwrp as fetch
import airquality.database.operation.insert.init as ins
import airquality.database.operation.select.sensor as sel_type
import container.sensor as sens_adapt
import airquality.adapter.api2db.measure as meas_adapt
import airquality.filter.basefilt as flt
import airquality.logger.util.decorator as log_decorator


class InitCommand(c.Command):

    ################################ __init__ ###############################
    def __init__(self,
                 fetch_wrapper: fetch.FetchWrapper,
                 insert_wrapper: ins.InitializeInsertWrapper,
                 select_type_wrapper: sel_type.TypeSelectWrapper,
                 api2db_adapter: Union[sens_adapt.SensorContainerBuilder, meas_adapt.MeasureAdapter],
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

        # Fetch API data
        sensor_data = self.fetch_wrapper.get_sensor_data()
        if not sensor_data:
            self.log_warning(f"{InitCommand.__name__}: empty API sensor data => no sensor inserted")
            return

        # Query the max 'sensor_id' for knowing the 'sensor_id' during the insertion
        max_sensor_id = self.select_type_wrapper.get_max_sensor_id()

        # Reshape API data
        sensor_containers = []
        for data in sensor_data:
            sensor_containers.append(self.api2db_adapter.raw2container(data=data, sensor_id=max_sensor_id))
            max_sensor_id += 1

        # Database sensor names associated to current sensor type
        database_sensor_names = self.select_type_wrapper.get_sensor_names()
        if database_sensor_names:

            # Create SensorDataFilter
            sensor_data_filter = flt.NameFilter(database_sensor_names=database_sensor_names, log_filename=self.log_filename)
            sensor_data_filter.set_file_logger(self.file_logger)
            sensor_data_filter.set_console_logger(self.console_logger)

            # Filter sensor data
            sensor_containers = sensor_data_filter.filter(containers=sensor_containers)
            if not sensor_containers:
                self.log_warning(f"{InitCommand.__name__}: all sensors are already present into the database => no sensor inserted")
                return

        # Execute queries on sensors
        self.insert_wrapper.insert(sensor_data=sensor_containers, sensor_id=max_sensor_id)
