######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 12/11/21 10:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.io.remote.database.adapter as db
import airquality.data.extractor.api as extr
import airquality.utility.picker.query as pk
import airquality.utility.parser.text as txt
import airquality.data.reshaper.uniform.api2db as a2d
import airquality.data.reshaper.uniform.db2api as d2a
import airquality.data.builder.url as u
import airquality.data.builder.geom as gb
import airquality.data.builder.timest as ts


class BaseBot(abc.ABC):

    def __init__(self,
                 sensor_type: str,
                 dbconn: db.DatabaseAdapter,
                 log_filename='',
                 log_sub_dir=''):

        self.sensor_type = sensor_type
        self.dbconn = dbconn
        self.timest_fmt = None
        self.current_ts = None
        self.url_builder = None
        self.query_picker = None
        self.api_extr_class = None
        self.text_parser_class = None
        self.api2db_rshp_class = None
        self.db2api_rshp_class = None
        self.geom_builder_class = None
        self.log_filename = log_filename
        self.log_sub_dir = log_sub_dir
        self.logger = None
        self.debugger = None

    ################################ METHODS FOR ADDING EXTERNAL DEPENDENCIES ################################
    def add_text_parser_class(self, text_parser_class: txt.TextParser):
        self.text_parser_class = text_parser_class

    def add_query_picker(self, query_picker: pk.QueryPicker):
        self.query_picker = query_picker

    def add_url_builder(self, url_builder: u.URLBuilder):
        self.url_builder = url_builder

    def add_api_extractor_class(self, api_extr_class=extr.APIExtractor):
        self.api_extr_class = api_extr_class

    def add_api2db_rshp_class(self, api2db_rshp_class=a2d.UniformReshaper):
        self.api2db_rshp_class = api2db_rshp_class

    def add_db2api_rshp_class(self, db2api_rshp_class=d2a.UniformReshaper):
        self.db2api_rshp_class = db2api_rshp_class

    def set_timest_fmt(self, fmt: str):
        self.timest_fmt = fmt

    def add_geom_builder_class(self, geom_builder_class: gb.GeometryBuilder):
        self.geom_builder_class = geom_builder_class

    def add_current_ts(self, current_ts: ts.CurrentTimestamp):
        self.current_ts = current_ts

    def add_logger(self, logger):
        self.logger = logger

    def add_debugger(self, debugger):
        self.debugger = debugger

    ################################ ABSTRACT METHODS ################################
    @abc.abstractmethod
    def run(self):
        pass
