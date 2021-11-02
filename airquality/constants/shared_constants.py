#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 16:43
# @Description: this script defines the constants shared in all modules of the project
#
#################################################


################################ DEFINE VALID PERSONALITIES FOR 'SENSOR AT LOCATION' ################################

PURPLEAIR_PERSONALITY = "purpleair"
THINGSPEAK_PERSONALITY = "thingspeak"
ATMOTUBE_PERSONALITY = "atmotube"

VALID_PERSONALITIES = (PURPLEAIR_PERSONALITY, THINGSPEAK_PERSONALITY, ATMOTUBE_PERSONALITY)
SENSOR_AT_LOCATION_PERSONALITIES = (PURPLEAIR_PERSONALITY,)
MOBILE_SENSOR_PERSONALITIES = (ATMOTUBE_PERSONALITY,)

################################ PATH OF THE FILES USED IN THE PROJECT ################################

API_FILE = "properties/api.json"
SERVER_FILE = "properties/server.json"
QUERY_FILE = "properties/sql_query.json"

################################ OUTPUT FORMAT CONSTANTS ################################

DEBUG_HEADER = "[DEBUG]:"
INITIALIZE_USAGE = "USAGE: python -m initialize [--help or -h] [--debug  or -d] personality api_address_number"
FETCH_USAGE = "USAGE: python -m fetch [--help or -h] [--debug  or -d] personality api_address_number"
GEO_USAGE = "USAGE: python -m geo [--help or -h] [--debug  or -d] personality api_address_number"

################################ EMPTY CONSTANTS ################################

EMPTY_STRING = ""
EMPTY_LIST = []
EMPTY_DICT = {}

################################ VALID ATMOTUBE API PARAMETERS ################################

ATMOTUBE_DATE_PARAM = "date"
ATMOTUBE_TIME_PARAM = "time"
ATMOTUBE_COORDS_PARAM = "coords"
ATMOTUBE_API_KEY_PARAM = 'api_key'
ATMOTUBE_MAC_PARAM = 'mac'
ATMOTUBE_ORDER_PARAM = 'order'

################################ VALID PURPLE AIR API PARAM ################################

PURPLEAIR_NAME_PARAM = "name"
PURPLEAIR_SENSOR_IDX_PARAM = "sensor_index"
PURPLEAIR_FIELDS_PARAM = "fields"
PURPLEAIR_DATA_PARAM = "data"
PURPLEAIR_CH_ID_PARAM = "channel_id"

################################ VALID ATMOTUBE API PARAM ################################


################################ PICKER-TO-QUERY_BUILDER CONSTANTS ################################

RESHAPER2SQLBUILDER_PARAM_ID = "par_id"
RESHAPER2SQLBUILDER_SENSOR_ID = "sens_id"
RESHAPER2SQLBUILDER_PARAM_VAL = "par_val"
RESHAPER2SQLBUILDER_TIMESTAMP = "ts"
RESHAPER2SQLBUILDER_GEOMETRY = "geom"

################################ MESSAGE ################################

SENSOR_NAME = "name"
PURPLE_AIR_API_PARAM = ["primary_id_a", "primary_key_a", "primary_id_b", "primary_key_b",
                        "secondary_id_a", "secondary_key_a", "secondary_id_b", "secondary_key_b"]
PURPLEAIR_LAT_PARAM = "latitude"
PURPLEAIR_LON_PARAM = "longitude"
PURPLE_AIR_GEO_PARAM = ["name", "sensor_index", PURPLEAIR_LAT_PARAM, PURPLEAIR_LON_PARAM]

################################ GEOMETRY BUILDER CONSTANTS ################################

GEOMBUILDER_LATITUDE = "latitude"
GEOMBUILDER_LONGITUDE = "longitude"

################################ POSTGIS GEOMETRY TYPE ################################

GEO_TYPE_ST_POINT_2D = "POINT({lon} {lat})"

################################ POSTGIS SRID CONSTANTS ################################

EPSG_SRID = 26918

################################ DATETIME REGULAR EXPRESSION PATTERN ################################

ATMOTUBE_DATETIME_REGEX_PATTERN = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z'
SQL_TIMESTAMP_REGEX_PATTERN = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
THINGSPEAK_DATETIME_REGEX_PATTERN = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'

################################ DATETIME FORMAT FOR DATETIME2STR CONVERSION ################################

DATETIME2SQLTIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

############# THINGSPEAK API PARAM FOR STORING LAST ACQUISITION TIMESTAMP FOR EACH CHANNEL ################

THINGSPEAK_TIMESTAMP_1A = "primary_timestamp_a"
THINGSPEAK_TIMESTAMP_1B = "primary_timestamp_b"
THINGSPEAK_TIMESTAMP_2A = "secondary_timestamp_a"
THINGSPEAK_TIMESTAMP_2B = "secondary_timestamp_b"

################################ THINGSPEAK API PARAM2PICK ################################
"""Pay attention to the order of this variable inside the list: remember to put channel id and channel key in the same
list index: these are going to be used by the Database2APIReshaper."""

THINGSPEAK_CH_ID_2PICK = ["primary_id_a", "primary_id_b", "secondary_id_a", "secondary_id_b"]
THINGSPEAK_KEY_2PICK = ["primary_key_a", "primary_key_b", "secondary_key_a", "secondary_key_b"]
THINGSPEAK_TS_2PICK = [THINGSPEAK_TIMESTAMP_1A, THINGSPEAK_TIMESTAMP_1B, THINGSPEAK_TIMESTAMP_2A,
                       THINGSPEAK_TIMESTAMP_2B]

################################ THINGSPEAK 2 DATABASE PARAM NAME MAPPING ################################

THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A = {"PM1.0 (ATM)": "pm1.0_atm_a", "PM2.5 (ATM)": "pm2.5_atm_a",
                                             "PM10.0 (ATM)": "pm10.0_atm_a", "Temperature": "temperature_a",
                                             "Humidity": "humidity_a"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B = {"PM1.0 (ATM)": "pm1.0_atm_b", "PM2.5 (ATM)": "pm2.5_atm_b",
                                             "PM10.0 (ATM)": "pm10.0_atm_b", "Pressure": "pressure_b"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A = {"0.3um": "0.3_um_count_a", "0.5um": "0.5_um_count_a",
                                             "1.0um": "1.0_um_count_a", "2.5um": "2.5_um_count_a",
                                             "5.0um": "5.0_um_count_a", "10.0um": "10.0_um_count_a"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B = {"0.3um": "0.3_um_count_b", "0.5um": "0.5_um_count_b",
                                             "1.0um": "1.0_um_count_b", "2.5um": "2.5_um_count_b",
                                             "5.0um": "5.0_um_count_b", "10.0um": "10.0_um_count_b"}

################################ THINGSPEAK API PACKET RESHAPER CONSTANTS ################################

THINGSPEAK_API_RESHAPER_TIME = "time"

################################ THINGSPEAK API DECODE CONSTANTS ################################

THINGSPEAK_API_DECODE_FEEDS = "feeds"
THINGSPEAK_API_DECODE_CHANNEL = "channel"
THINGSPEAK_API_DECODE_NAME = "name"
THINGSPEAK_API_DECODE_CREATED_AT = "created_at"
THINGSPEAK_CHANNEL_DECODE = "_b"
THINGSPEAK_COUNTERS_DECODE = "Counters"

################################ OPTIONAL API PARAMETERS TO PICK FROM API DATA ################################

ATMOTUBE_OPTIONAL_API_PARAM = ['order']
ATMOTUBE_START_FETCH_TIMESTAMP = '2021-01-01 00:00:00'
THINGSPEAK_START_FETCH_TIMESTAMP = '2018-01-01 00:00:00'
