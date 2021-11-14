######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 12/11/21 10:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.api.util.extractor as extr
import airquality.file.util.parser as txt
import airquality.adapter.api2db.sensor as sens
import airquality.adapter.db2api.param as par
import airquality.adapter.api2db.measure as meas
import airquality.api.util.url as u
import airquality.bot.util.executor as ex
import airquality.bot.util.filter as filt


class BaseBot(abc.ABC):

    def __init__(self, log_filename='', log_sub_dir=''):

        self.url_builder = None
        self.api_extr_class = None
        self.param_rshp_class = None
        self.sensor_rshp_class = None
        self.measure_rshp_class = None
        self.text_parser_class = None
        self.bot_query_executor = None
        self.packet_executor = None
        self.packet_filter = None
        self.log_filename = log_filename
        self.log_sub_dir = log_sub_dir
        self.logger = None
        self.debugger = None

    ################################ METHODS FOR ADDING EXTERNAL DEPENDENCIES ################################
    def add_text_parser_class(self, text_parser_class: txt.TextParser):
        self.text_parser_class = text_parser_class

    def add_packet_filter(self, pck_filter: filt.PacketFilter):
        self.packet_filter = pck_filter

    def add_bot_query_executor(self, executor: ex.BotQueryExecutor):
        self.bot_query_executor = executor

    def add_packet_query_executor(self, executor: ex.PacketQueryExecutor):
        self.packet_executor = executor

    def add_url_builder(self, url_builder: u.URLBuilder):
        self.url_builder = url_builder

    def add_api_extractor_class(self, api_extr_class=extr.APIExtractor):
        self.api_extr_class = api_extr_class

    def add_sensor_rshp_class(self, sensor_rshp_class=sens.SensorAdapter):
        self.sensor_rshp_class = sensor_rshp_class

    def add_measure_rshp_class(self, measure_rshp_class=meas.MeasureAdapter):
        self.measure_rshp_class = measure_rshp_class

    def add_param_rshp_class(self, param_rshp_class=par.ParamAdapter):
        self.param_rshp_class = param_rshp_class

    def add_logger(self, logger):
        self.logger = logger

    def add_debugger(self, debugger):
        self.debugger = debugger

    ################################ ABSTRACT METHODS ################################
    @abc.abstractmethod
    def run(self):
        pass
