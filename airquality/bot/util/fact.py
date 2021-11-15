######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 12/11/21 16:20
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.bot.init as init
import airquality.bot.fetch as fetch
import airquality.bot.update as update


def get_bot_class(bot_name: str):

    if bot_name == 'init':
        return init.InitializeBot
    elif bot_name == 'update':
        return update.UpdateBot
    elif bot_name == 'fetch':
        return fetch.FetchBot
