######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 11/11/21 12:48
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
import time
from typing import List

# IMPORT MODULES
import airquality.core.logger.log as log
import airquality.bot.date_fetch_bot as dfb
import airquality.bot.fetch_bot as fb
import airquality.io.local.io as io
import airquality.io.remote.database.adapter as db
import airquality.utility.picker.query as pk
import airquality.utility.parser.file as fp
import airquality.data.builder.timest as ts
import airquality.data.builder.url as url
import airquality.data.reshaper.packet as rshp
import airquality.data.reshaper.uniform.api2db as a2d
import airquality.data.reshaper.uniform.db2api as d2a

# IMPORT CONSTANTS
import airquality.core.constants.system_constants as sc
from airquality.core.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, VALID_PERSONALITIES

USAGE = "python(version) -m airquality bot_name sensor_type"
VALID_NAMES = ("init", "update", "fetch")
VALID_TYPES = ('purpleair', 'thingspeak', 'atmotube')

################################ DEBUGGER AND LOGGER VARIABLES ################################
debugger = log.get_logger(use_color=True)
logger = log.get_logger(log_filename=f"{__name__}", log_sub_dir="log")


################################ ENTRY POINT OF THE PROGRAM ################################
def main():

    try:
        args = sys.argv[1:]
        if not args:
            raise SystemExit(f"wrong usage => {USAGE}")

        # Retrieve 'bot_name' and 'sensor_type' arguments
        bot_name = args[0] if args[0] in VALID_NAMES else ""
        sensor_type = args[1] if args[1] in VALID_TYPES else ""
        main_settings_msg = f"bot_name={bot_name}, sensor_type={sensor_type}"

        # Arguments checking
        if not bot_name or not sensor_type:
            raise SystemExit(f"bad arguments => valid names: {VALID_NAMES!s}, valid_types: {VALID_TYPES!s}")

        # Bot checking
        if bot_name == 'init':
            if sensor_type not in ('purpleair', ):
                raise SystemExit(f"bad personality => '{bot_name}' bot is not available for '{sensor_type}' sensors")
        elif bot_name == 'update':
            if sensor_type not in ('purpleair',):
                raise SystemExit(f"bad personality => '{bot_name}' bot is not available for '{sensor_type}' sensors")
        elif bot_name == 'fetch':
            if sensor_type not in ('atmotube', 'thingspeak', ):
                raise SystemExit(f"bad personality => '{bot_name}' bot is not available for '{sensor_type}' sensors")

        # Logging when it's all right
        debugger.info(main_settings_msg)
        logger.info(main_settings_msg)

    except SystemExit as ex:
        debugger.error(str(ex))
        logger.error(str(ex))
        sys.exit(1)
