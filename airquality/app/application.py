######################################################
#
# Author: Davide Colombo
# Date: 11/11/21 12:48
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import dotenv

# IMPORT MODULES
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator
import airquality.app.util.args as arg
import airquality.app.util.make as make
import airquality.bot.util.fact as fact
import airquality.api.fetch as api_op
import airquality.file.structured.json as jf
import airquality.api.util.extractor as ext
import airquality.api.util.url as url
import airquality.database.util.conn as db_conn
import database.util.query as qry
import airquality.file.util.parser as parser
import airquality.adapter.api2db.sensor as sens
import airquality.adapter.db2api.param as par
import airquality.adapter.api2db.measure as meas
import airquality.database.operation.insert as insert_op
import airquality.database.operation.select as select_op
import airquality.bot.util.datelooper as loop
import airquality.bot.util.filter as filt

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

        # TextParser
        text_parser = parser.get_text_parser(file_ext=file_extension)
        self.info_messages.append(f"text_parser_class={text_parser.__class__.__name__}")

        # URLBuilder
        url_class = url.get_url_class(self.sensor_type)
        url_builder = url_class(address=address, url_param=url_param)
        self.info_messages.append(f"url_builder_class={url_class.__name__}")

        # APIExtractor class
        data_extractor = ext.get_data_extractor(self.sensor_type)
        self.info_messages.append(f"data_extractor_class={data_extractor.__class__.__name__}")

        # Sensor's API FetchWrapper
        fetch_wrapper = api_op.FetchWrapper(url_builder=url_builder, data_extractor=data_extractor,
                                            response_parser=text_parser)
        bot.add_fetch_wrapper(fetch_wrapper)

        ################################ INJECT DATABASE DEPENDENCIES ################################
        # DatabaseAdapter class
        db_adapter = db_conn.Psycopg2DatabaseAdapter(connection_string=os.environ['DBCONN'])

        # QueryBuilder class
        file_object = jf.JSONFile(QUERY_FILE)
        query_builder = qry.QueryBuilder(file_object)

        # InsertionOperation class
        insert_operation = insert_op.get_insert_wrapper(self.sensor_type, conn=db_adapter, builder=query_builder)
        insert_operation.set_debugger(self.debugger)
        insert_operation.set_logger(logger)
        bot.add_insert_wrapper(insert_operation)
        self.info_messages.append(f"insert_wrapper_class={insert_operation.__class__.__name__}")

        # SelectFromSensorID operation dependency
        if self.bot_name == 'fetch':
            select_from_sensor_id_operation = select_op.SensorIDSelectWrapper(conn=db_adapter,
                                                                              query_builder=query_builder)
            bot.add_sensor_id_select_wrapper(select_from_sensor_id_operation)
            self.info_messages.append(
                f"sensor_id_select_wrapper_class={select_from_sensor_id_operation.__class__.__name__}")

        # SelectFromSensorType operation dependency
        sensor_type_select_wrapper = select_op.SensorTypeSelectWrapper(
            conn=db_adapter,
            query_builder=query_builder,
            sensor_type=self.sensor_type
        )
        sensor_type_select_wrapper.set_logger(logger)
        sensor_type_select_wrapper.set_debugger(self.debugger)
        bot.add_sensor_type_select_wrapper(sensor_type_select_wrapper)
        self.info_messages.append(f"sensor_type_select_wrapper_class={sensor_type_select_wrapper.__class__.__name__}")

        ################################ INJECT OTHER DEPENDENCIES ################################

        # PacketFilter class
        packet_filter = filt.get_packet_filter(self.bot_name)
        packet_filter.set_debugger(self.debugger)
        packet_filter.set_logger(logger)
        bot.add_packet_filter(packet_filter)
        self.info_messages.append(f"packet_filter_class={packet_filter.__class__.__name__}")

        ################################ INJECT ADAPTER DEPENDENCIES ################################

        if self.bot_name in ('init', 'update'):

            # SensorAdapter
            sensor_adapter = sens.get_sensor_adapter(self.sensor_type)
            bot.add_api2database_adapter(sensor_adapter)
            self.info_messages.append(f"sensor_adapter_class={sensor_adapter.__class__.__name__}")

        elif self.bot_name == 'fetch':

            # Get the start measure id
            start_measure_id = select_op.get_max_measure_id(
                sensor_type=self.sensor_type,
                sensor_type_select_wrapper=sensor_type_select_wrapper)

            # Query the (param_code, param_id) tuples for the measure param associated to 'sensor_type'
            measure_param_map = sensor_type_select_wrapper.get_measure_param()

            # MeasureAdapter
            measure_adapter = meas.get_measure_adapter(
                sensor_type=self.sensor_type,
                start_id=start_measure_id,
                measure_param_map=measure_param_map
            )

            bot.add_api2database_adapter(measure_adapter)
            self.info_messages.append(f"measure_adapter_class={measure_adapter.__class__.__name__}")

            # ParamAdapter
            param_adapter = par.get_param_adapter(self.sensor_type)
            bot.add_db2api_adapter(param_adapter)
            self.info_messages.append(f"param_adapter_class={param_adapter.__class__.__name__}")
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
