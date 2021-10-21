#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 19:11
# @Description: this script defines the classes that use database and sensor APIs.
#
#################################################
import builtins
from abc import ABC


class BaseBot(ABC):
    """Abstract Base Class for bot objects."""
    pass


class BotAtmotube(BaseBot):

    def __init__(self):
        pass



################################ FACTORY ################################
class BotFactory(builtins.object):


    @staticmethod
    def create_bot_from_personality(bot_personality: str) -> BaseBot:

        if bot_personality == "atmotube":
            return BotAtmotube()
        else:
            raise SystemExit(f"{BotFactory.__name__}: invalid bot personality {bot_personality}.")
