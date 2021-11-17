######################################################
#
# Author: Davide Colombo
# Date: 11/11/21 12:48
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
# --------------------- BUILTIN IMPORT ---------------------
import os
import dotenv
# --------------------- LOGGER IMPORT ---------------------
# log
import airquality.logger.loggable as log
# util
import airquality.logger.util.decorator as log_decorator
# --------------------- APPLICATION IMPORT ---------------------
# util
import airquality.app.util.args as arg
import airquality.app.util.make as make
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
import airquality.database.operation.select as select
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

        ################################ LOADING '.env' FILE ################################
        dotenv.load_dotenv(dotenv_path="./properties/.env")
        arg.exit_on_bad_env_param()

        ################################ BOT SPECIFIC LOGGER ################################
        logger = make.make_file_logger(file_path=f'log/{self.bot_name}.log')

        ################################ MAKE BOT CLASS ################################
        bot_class = fact.get_bot_class(self.bot_name)
        bot = bot_class(log_filename=self.bot_name, log_sub_dir='log')
        self.info_messages.append(f"bot_class={bot_class.__name__}")

        ################################ INJECT API DEPENDENCIES ################################
        api_file_object = jf.JSONFile(API_FILE, path_to_object=[self.sensor_type])
        address = api_file_object.api_address
        url_param = api_file_object.url_param
        arg.exit_on_bad_api_param(url_param=url_param, sensor_type=self.sensor_type)

        # Append secret 'api_key' for purpleair sensor from '.env' file
        if self.sensor_type == 'purpleair':
            api_key = os.environ['PURPLEAIR_KEY1']
            url_param.update({'api_key': api_key})

        # file extension for building the TextParser
        file_extension = "json"
        if self.sensor_type in ('atmotube', 'thingspeak',):
            file_extension = url_param['format']

        ################################ INJECT API DEPENDENCIES ################################
        # TextParser for parsing API responses
        response_parser = parser.get_text_parser(file_ext=file_extension)

        # URLBuilder
        url_builder = url.get_url_builder(
            sensor_type=self.sensor_type,
            address=address,
            url_param=url_param)

        # APIExtractor class
        data_extractor = ext.get_data_extractor(sensor_type=self.sensor_type)

        # FetchWrapper
        fetch_wrapper = fetch.FetchWrapper(
            url_builder=url_builder,
            extractor=data_extractor,
            parser=response_parser)

        # Inject logger and debugger
        fetch_wrapper.set_logger(logger)
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
        insert_wrapper.set_logger(logger)
        insert_wrapper.set_debugger(self.debugger)

        # Setup for 'init' and 'update' bots
        if self.bot_name in ('init', 'update'):
            insert_wrapper.set_sensor_record_builder(builder=rec.SensorRecord())
            insert_wrapper.set_api_param_record_builder(builder=rec.APIParamRecord())
            insert_wrapper.set_sensor_info_record_builder(
                builder=rec.SensorInfoRecord(time_rec=time_rec))
            insert_wrapper.set_sensor_location_record_builder(
                builder=rec.SensorLocationRecord(location_rec=location_rec, time_rec=t.CurrentTimestampTimeRecord()))
        elif self.bot_name == 'fetch':
            if self.sensor_type == 'atmotube':
                insert_wrapper.set_mobile_record_builder(
                    builder=rec.MobileMeasureRecord(time_rec=time_rec, location_rec=location_rec))
            elif self.sensor_type == 'thingspeak':
                insert_wrapper.set_station_record_builder(builder=rec.StationMeasureRecord(time_rec=time_rec))

        # Inject InsertWrapper to Bot
        bot.add_insert_wrapper(insert_wrapper)
        self.info_messages.append(f"insert_wrapper_class={insert_wrapper.__class__.__name__}")

        ################################ SETUP SELECT WRAPPERS ################################
        # SensorIDSelectWrapper
        if self.bot_name == 'fetch':
            sensor_id_select_wrapper = select.SensorIDSelectWrapper(conn=conn, query_builder=query_builder)
            bot.add_sensor_id_select_wrapper(sensor_id_select_wrapper)
            self.info_messages.append(f"sensor_id_select_wrapper_class={sensor_id_select_wrapper.__class__.__name__}")

        # SensorTypeSelectWrapper
        sensor_type_select_wrapper = select.SensorTypeSelectWrapper(
            conn=conn,
            query_builder=query_builder,
            sensor_type=self.sensor_type)

        # Inject logger and debugger
        sensor_type_select_wrapper.set_logger(logger)
        sensor_type_select_wrapper.set_debugger(self.debugger)

        # Inject SensorTypeSelectWrapper to Bot
        bot.add_sensor_type_select_wrapper(sensor_type_select_wrapper)
        self.info_messages.append(f"sensor_type_select_wrapper_class={sensor_type_select_wrapper.__class__.__name__}")

        ################################ SENSOR DATA FILTER DEPENDENCIES ################################

        # SensorDataFilter
        sensor_data_filter = filt.get_sensor_data_filter(bot_name=self.bot_name, sensor_type=self.sensor_type)
        sensor_data_filter.set_debugger(self.debugger)
        sensor_data_filter.set_logger(logger)
        bot.add_sensor_data_filter(sensor_data_filter)
        self.info_messages.append(f"packet_filter_class={sensor_data_filter.__class__.__name__}")

        # Add GeoFilter
        if self.bot_name == 'update':
            postgis_builder = geom.PointBuilder()
            geo_filter = filt.GeoFilter(postgis_builder)
            bot.add_geo_filter(geo_filter)

        ################################ INJECT ADAPTER DEPENDENCIES ################################

        if self.bot_name in ('init', 'update'):

            # Inject SensorAdapter to Bot
            bot.add_api2database_adapter(adapter=sens.get_sensor_adapter(sensor_type=self.sensor_type))

        elif self.bot_name == 'fetch':

            # Query the start record ID
            start_measure_id = select.get_max_measure_id(
                sensor_type=self.sensor_type,
                sensor_type_select_wrapper=sensor_type_select_wrapper)

            # Query the (param_code, param_id) tuples for the measure param associated to 'sensor_type'
            measure_param_map = sensor_type_select_wrapper.get_measure_param()

            measure_adapter = meas.get_measure_adapter(
                    sensor_type=self.sensor_type,
                    start_id=start_measure_id,
                    measure_param_map=measure_param_map
                )

            # Inject MeasureAdapter to Bot
            bot.add_api2database_adapter(adapter=measure_adapter)

            # Inject APIParamAdapter to Bot
            bot.add_db2api_adapter(adapter=par.get_param_adapter(sensor_type=self.sensor_type))

        ################################ END ADAPTER DEPENDENCIES ################################

        # Add DateLooper dependency
        if self.bot_name == 'fetch':
            date_looper_class = loop.get_date_looper_class(self.sensor_type)
            bot.add_date_looper_class(date_looper_class)
            self.info_messages.append(f"date_looper_class={date_looper_class.__name__}")

        # Set logger and debugger
        bot.set_logger(logger)
        bot.set_debugger(self.debugger)

        self.bot = bot
