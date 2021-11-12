######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 11/11/21 20:29
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.bot.init as init
import airquality.bot.fetch as fetch
import airquality.bot.update as update

VALID_NAMES = ("init", "update", "fetch")
VALID_TYPES = ('purpleair', 'thingspeak', 'atmotube')


def get_bot_class(bot_name: str, sensor_type: str):

    err_msg = f"'{get_bot_class.__name__}()': bad '{sensor_type}' type for '{bot_name}' bot => "
    if bot_name == 'init':
        if sensor_type in ('purpleair', ):
            return init.InitializeBot
        else:
            err_msg += f"the only valid type for '{bot_name}' bot is: ['purpleair']"
    elif bot_name == 'update':
        if sensor_type in ('purpleair', ):
            return update.UpdateBot
        else:
            err_msg += f"the only valid type for '{bot_name}' bot is: ['purpleair']"
    elif bot_name == 'fetch':
        if sensor_type in ('atmotube', 'thingspeak', ):
            return fetch.FetchBot
        else:
            err_msg += f"the valid types for '{bot_name}' bot are: ['atmotube', 'thingspeak']"

    # If the interpreter arrive here, it means that the combination of 'bot_name' and 'sensor_type' is wrong
    raise SystemExit(err_msg)
