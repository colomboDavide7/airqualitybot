######################################################
#
# Author: Davide Colombo
# Date: 12/11/21 16:20
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.bot.init as init
import airquality.bot.fetch as fetch
import airquality.bot.update as update


def get_bot(bot_name: str, log_filename="app"):

    if bot_name == 'init':
        return init.InitializeBot(log_filename=log_filename)
    elif bot_name == 'update':
        return update.UpdateBot(log_filename=log_filename)
    elif bot_name == 'fetch':
        return fetch.FetchBot(log_filename=log_filename)
    else:
        raise SystemExit(f"'{get_bot.__name__}():' bad name '{bot_name}'")
