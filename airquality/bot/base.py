######################################################
#
# Author: Davide Colombo
# Date: 12/11/21 10:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.loggable as log
import airquality.api.fetchwrp as fetch
import airquality.database.operation.select.sensor as sel_type
import airquality.database.operation.baseoprt as base_wrp
import airquality.filter.basefilt as filt


class BaseBot(log.Loggable):

    def __init__(self, log_filename="app"):
        super(BaseBot, self).__init__(log_filename=log_filename)
        self.db2api_adapter = None
        self.api2db_adapter = None
        self.sensor_type_select_wrapper = None
        self.insert_wrapper = None
        self.sensor_data_filter = None
        self.fetch_wrapper = None

    ################################ METHODS FOR ADDING EXTERNAL DEPENDENCIES ################################
    def add_fetch_wrapper(self, wrapper: fetch.FetchWrapper):
        self.fetch_wrapper = wrapper

    def add_sensor_data_filter(self, data_filter: filt.BaseFilter):
        self.sensor_data_filter = data_filter

    ################################ INJECT EXECUTOR DEPENDENCIES ################################
    def add_sensor_type_select_wrapper(self, wrapper: sel_type.TypeSelectWrapper):
        self.sensor_type_select_wrapper = wrapper

    def add_insert_wrapper(self, wrapper: base_wrp.DatabaseOperationWrapper):
        self.insert_wrapper = wrapper

    ################################ INJECT ADAPTER DEPENDENCIES ################################
    def add_api2database_adapter(self, adapter):
        """Adapter is one within SensorAdapter or MeasureAdapter"""
        self.api2db_adapter = adapter

    def add_db2api_adapter(self, adapter):
        """Adapter argument is ParamAdapter"""
        self.db2api_adapter = adapter

    ################################ ABSTRACT METHODS ################################
    @abc.abstractmethod
    def execute(self):
        pass
