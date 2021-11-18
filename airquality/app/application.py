######################################################
#
# Author: Davide Colombo
# Date: 11/11/21 12:48
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
# --------------------- BUILTIN IMPORT ---------------------
import os
# --------------------- LOGGER IMPORT ---------------------
# log
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator
# --------------------- BOT IMPORT ---------------------
# util
import airquality.bot.util.fact as fact
import airquality.bot.util.datelooper as loop
# --------------------- FILTER IMPORT ---------------------
import airquality.filter.filter as filt
# --------------------- FILE IMPORT ---------------------
# structured
import airquality.file.structured.json as jf
# util
import airquality.file.util.parser as parser
import airquality.file.util.loader as loader
# --------------------- ADAPTER IMPORT ---------------------
import airquality.adapter.api2db.sensor as sens
import airquality.adapter.api2db.measure as meas
import airquality.adapter.db2api.param as par
# --------------------- API IMPORT ---------------------
# fetch
import airquality.api.fetch as fetch
# util
import airquality.api.util.url as url
import airquality.api.util.extractor as ext
# --------------------- DATABASE IMPORT ---------------------
# operation
import airquality.database.operation.select.type as sel_type
import airquality.database.operation.insert as insert
# util
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.record.time as t
import airquality.database.util.record.location as loc
import airquality.database.util.record.record as rec
import airquality.database.util.postgis.geom as geom
import airquality.database.util.conn as db_conn
import airquality.database.util.query as qry


################################ GLOBAL VARIABLES ################################

ENV_FILE = 'properties/.env'
API_FILE = "properties/api.json"
QUERY_FILE = "properties/query.json"


################################ APPLICATION CLASS ################################
class Application(log.Loggable):

    def __init__(self, bot_name: str, sensor_type: str):
        super(Application, self).__init__()
        self.bot_name = bot_name
        self.sensor_type = sensor_type
        self.log_filename = bot_name
        self.log_sub_dir = 'log'
        self.bot = None

    @log_decorator.log_decorator()
    def run(self):
        if not self.bot:
            raise SystemExit(f"{Application.__name__}: bad setup => bot is None")
        self.bot.execute()
        self.bot.log_messages()

    @log_decorator.log_decorator()
    def setup(self):

        ############################ READ API FILE AND GET PARAM ASSOCIATED TO SENSOR TYPE #############################
        file_obj = jf.JSONFile(API_FILE, path_to_object=[self.sensor_type])
        address, url_param, file_ext = loader.get_api_param_from_file(sensor_type=self.sensor_type, file_object=file_obj)

        ################################ LOADING '.env' FILE ################################
        loader.load_environment_file(file_path=ENV_FILE, sensor_type=self.sensor_type)

        # Append secret 'api_key' for purpleair sensor from '.env' file
        if self.sensor_type == 'purpleair':
            url_param.update({'api_key': os.environ['PURPLEAIR_KEY1']})

        ################################ MAKE BOT ################################
        bot = fact.get_bot(self.bot_name, log_filename=self.bot_name, log_sub_dir='log')

        ################################ INJECT API DEPENDENCIES ################################
        response_parser = parser.get_text_parser(file_ext=file_ext)
        url_builder = url.get_url_builder(sensor_type=self.sensor_type, address=address, url_param=url_param)
        data_extractor = ext.get_data_extractor(sensor_type=self.sensor_type)

        # FetchWrapper
        fetch_wrapper = fetch.FetchWrapper(url_builder=url_builder, extractor=data_extractor, parser=response_parser)
        fetch_wrapper.set_logger(self.logger)
        fetch_wrapper.set_debugger(self.debugger)

        # Inject dependency to Bot
        bot.add_fetch_wrapper(wrapper=fetch_wrapper)

        ################################ GET DATABASE OBJECTS ################################
        # Database Utilities
        conn = db_conn.Psycopg2DatabaseAdapter(connection_string=os.environ['DBCONN'])
        query_builder = qry.QueryBuilder(query_file=jf.JSONFile(QUERY_FILE))

        # RecordBuilder
        time_rec = t.TimeRecord(timestamp_class=ts.get_timestamp_class(sensor_type=self.sensor_type))
        location_rec = loc.LocationRecord(postgis_builder=geom.PointBuilder())

        # InsertWrapper
        insert_wrapper = insert.get_insert_wrapper(sensor_type=self.sensor_type, conn=conn, builder=query_builder)

        ################################ SETUP INSERT WRAPPER ################################
        # Inject debugger and logger to InsertWrapper
        insert_wrapper.set_logger(self.logger)
        insert_wrapper.set_debugger(self.debugger)

        # Setup for 'init' and 'update' bots
        if self.bot_name in ('init', 'update'):
            insert_wrapper.set_sensor_record_builder(builder=rec.SensorRecord())
            insert_wrapper.set_api_param_record_builder(builder=rec.APIParamRecord())
            insert_wrapper.set_sensor_info_record_builder(builder=rec.SensorInfoRecord(time_rec=time_rec))
            insert_wrapper.set_sensor_location_record_builder(
                builder=rec.SensorLocationRecord(location_rec=location_rec, time_rec=t.CurrentTimestampTimeRecord())
            )

        elif self.bot_name == 'fetch':
            if self.sensor_type == 'atmotube':
                insert_wrapper.set_mobile_record_builder(
                    builder=rec.MobileMeasureRecord(time_rec=time_rec, location_rec=location_rec))
            elif self.sensor_type == 'thingspeak':
                insert_wrapper.set_station_record_builder(builder=rec.StationMeasureRecord(time_rec=time_rec))

        # Inject InsertWrapper to Bot
        bot.add_insert_wrapper(insert_wrapper)

        ################################ SETUP SELECT WRAPPERS ################################
        # SensorIDSelectWrapper
        if self.bot_name == 'fetch':
            sensor_id_select_wrapper = sel_type.SensorIDSelectWrapper(conn=conn, query_builder=query_builder)
            bot.add_sensor_id_select_wrapper(sensor_id_select_wrapper)

        # SensorTypeSelectWrapper
        type_select_wrapper = sel_type.get_type_select_wrapper(conn=conn, query_builder=query_builder, sensor_type=self.sensor_type)
        type_select_wrapper.set_logger(self.logger)
        type_select_wrapper.set_debugger(self.debugger)

        # Inject SensorTypeSelectWrapper to Bot
        bot.add_sensor_type_select_wrapper(type_select_wrapper)

        ################################ SENSOR DATA FILTER DEPENDENCIES ################################

        # SensorDataFilter
        sensor_data_filter = filt.get_sensor_data_filter(
            bot_name=self.bot_name,
            sensor_type=self.sensor_type,
            sel_wrapper=type_select_wrapper)

        # Set logger and debugger
        sensor_data_filter.set_debugger(self.debugger)
        sensor_data_filter.set_logger(self.logger)
        bot.add_sensor_data_filter(sensor_data_filter)

        ################################ INJECT ADAPTER DEPENDENCIES ################################

        if self.bot_name in ('init', 'update'):
            # SensorAdapter
            sensor_adapter = sens.get_sensor_adapter(sensor_type=self.sensor_type)
            bot.add_api2database_adapter(adapter=sensor_adapter)

        elif self.bot_name == 'fetch':
            # MeasureAdapter
            measure_adapter = meas.get_measure_adapter(sensor_type=self.sensor_type, type_wrapper=type_select_wrapper)
            bot.add_api2database_adapter(adapter=measure_adapter)

            # ParamAdapter
            param_adapter = par.get_param_adapter(sensor_type=self.sensor_type)
            bot.add_db2api_adapter(adapter=param_adapter)

        ################################ END ADAPTER DEPENDENCIES ################################

        # Add DateLooper dependency
        if self.bot_name == 'fetch':
            date_looper_class = loop.get_date_looper_class(self.sensor_type)
            bot.add_date_looper_class(date_looper_class)

        # Set logger and debugger
        bot.set_logger(self.logger)
        bot.set_debugger(self.debugger)

        self.bot = bot
