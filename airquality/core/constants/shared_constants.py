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
VALID_PERSONALITIES = (PURPLEAIR_PERSONALITY, ATMOTUBE_PERSONALITY, THINGSPEAK_PERSONALITY, )

################################ PATH OF THE FILES USED IN THE PROJECT ################################

API_FILE = "properties/api.json"
SERVER_FILE = "properties/server.json"
QUERY_FILE = "properties/query.json"

################################ OUTPUT FORMAT CONSTANTS ################################

INITIALIZE_USAGE = "USAGE: python -m initialize [--help or -h] [--debug  or -d] personality"
FETCH_USAGE = "USAGE: python -m fetch [--help or -h] [--debug  or -d] personality"
GEO_USAGE = "USAGE: python -m update [--help or -h] [--debug  or -d] personality"
