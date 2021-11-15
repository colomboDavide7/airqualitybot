######################################################
#
# Author: Davide Colombo
# Date: 12/11/21 10:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.loggable as log
import airquality.api.fetch as api_op
import airquality.database.operation.select as select_op
import airquality.database.operation.base as db_op_base
import airquality.bot.util.filter as filt


class BaseBot(log.Loggable):

    def __init__(self, log_filename: str, log_sub_dir: str):
        super(BaseBot, self).__init__()
        self.db2api_adapter = None
        self.api2db_adapter = None
        self.sensor_type_select_wrapper = None
        self.insert_wrapper = None
        self.packet_filter = None
        self.fetch_wrapper = None
        self.log_filename = log_filename
        self.log_sub_dir = log_sub_dir

    ################################ METHODS FOR ADDING EXTERNAL DEPENDENCIES ################################
    def add_fetch_wrapper(self, op: api_op.FetchWrapper):
        self.fetch_wrapper = op

    def add_packet_filter(self, pck_filter: filt.SensorDataFilter):
        self.packet_filter = pck_filter

    ################################ INJECT EXECUTOR DEPENDENCIES ################################
    def add_sensor_type_select_wrapper(self, op: select_op.SensorTypeSelectWrapper):
        self.sensor_type_select_wrapper = op

    def add_insert_wrapper(self, op: db_op_base.DatabaseOperationWrapper):
        self.insert_wrapper = op

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

    def safe_shut_down(self):
        # TODO: shut down database connection
        pass
