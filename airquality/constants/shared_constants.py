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

################################ ANSI ESCAPE CODES FOR COLOR IN TERMINAL ################################

GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"

################################ OUTPUT FORMAT CONSTANTS ################################

DEBUG_HEADER = f"{GREEN}[DEBUG]:{RESET}"
INFO_HEADER = f"{BLUE}[INFO]:{RESET}"
WARNING_HEADER = f"{YELLOW}[WARNING]:{RESET}"
EXCEPTION_HEADER = f"{RED}[EXCEPTION]:{RESET}"
INITIALIZE_USAGE = "USAGE: python -m initialize [--help or -h] [--debug  or -d] personality"
FETCH_USAGE = "USAGE: python -m fetch [--help or -h] [--debug  or -d] personality"
GEO_USAGE = "USAGE: python -m geo [--help or -h] [--debug  or -d] personality"

################################ EMPTY CONSTANTS ################################

EMPTY_STRING = ""

################################ DATETIME REGULAR EXPRESSION PATTERN ################################

ATMOTUBE_DATETIME_REGEX_PATTERN = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z'
SQL_TIMESTAMP_REGEX_PATTERN = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
THINGSPEAK_DATETIME_REGEX_PATTERN = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'

################################ DATETIME FORMAT FOR DATETIME2STR CONVERSION ################################

DATETIME2SQLTIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

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
