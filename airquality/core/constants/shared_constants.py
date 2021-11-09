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
QUERY_FILE = "properties/query.json"

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
