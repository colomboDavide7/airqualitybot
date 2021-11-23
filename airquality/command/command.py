######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 12:03
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Union
import airquality.logger.loggable as log
import airquality.api.fetch as fetch
import airquality.database.operation.insert.insert as ins
import airquality.database.operation.select.sensor as sel_type
import container.sensor as sens_adapt
import airquality.adapter.api2db.measure as meas_adapt


class Command(log.Loggable, abc.ABC):

    ################################ __init__ ###############################
    def __init__(self,
                 fetch_wrapper: fetch.FetchWrapper,
                 insert_wrapper: ins.InsertWrapper,
                 select_type_wrapper: sel_type.TypeSelectWrapper,
                 api2db_adapter: Union[sens_adapt.SensorContainerBuilder, meas_adapt.MeasureAdapter],
                 log_filename="log"):

        super(Command, self).__init__(log_filename=log_filename)
        self.fetch_wrapper = fetch_wrapper
        self.insert_wrapper = insert_wrapper
        self.select_type_wrapper = select_type_wrapper
        self.api2db_adapter = api2db_adapter

    ################################ execute ###############################
    @abc.abstractmethod
    def execute(self):
        pass
