#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 19:08
# @Description: unit test script
#
#################################################
import builtins
import unittest
from airquality.bot.bot import BotFactory


class TestBot(unittest.TestCase):


    def test_invalid_bot_personality(self):

        with self.assertRaises(SystemExit):
            BotFactory.create_bot_from_personality("bad_bot_personality")
            

    def test_system_exit_when_missing_api_adapter(self):

        bot = BotFactory.create_bot_from_personality("atmotube")
        bot.dbconn = builtins.object()
        bot.sqlbuilder = builtins.object()
        with self.assertRaises(SystemExit):
            bot.run()

    def test_system_exit_when_missing_dbconn_adapter(self):

        bot = BotFactory.create_bot_from_personality("atmotube")
        # Assign some object
        bot.apiadapter = builtins.object()
        with self.assertRaises(SystemExit):
            bot.run()

    def test_system_exit_when_missing_query_builder(self):

        bot = BotFactory.create_bot_from_personality("atmotube")
        # Assign some object
        bot.apiadapter = builtins.object()
        bot.dbconn = builtins.object()
        with self.assertRaises(SystemExit):
            bot.run()


if __name__ == '__main__':
    unittest.main()
