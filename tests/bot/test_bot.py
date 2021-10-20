#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 19:08
# @Description: Test script for testing the behaviour of the Bots
#
#################################################

import unittest
from airquality.bot.bot import BotFactory, BotMobile
from airquality.conn.conn import DatabaseConnection


class TestBot(unittest.TestCase):

    def setUp(self) -> None:
        """Set up method is used to create a DatabaseConnection instance
        since the BaseBot constructor takes 'dbconn' argument."""

        self.mobile_settings = {"port": 5432,
                                "dbname": "airquality",
                                "host": "localhost",
                                "username": "bot_mobile_user",
                                "password": None}
        self.mobile_dbconn = DatabaseConnection(self.mobile_settings)

    def test_create_bot_mobile(self):
        """Test the correct creation of the BotMobile instance."""
        user_type = "atmotube"
        bot = BotFactory.create_bot_from_type(user_type = user_type,
                                              dbconn = self.mobile_dbconn)
        self.assertIsNotNone(bot)
        self.assertIsInstance(bot, BotMobile)

    def test_type_error_bot_mobile(self):
        """Test TypeError when bad type is passed as argument."""
        user_type = "bad_user_type"
        with self.assertRaises(TypeError):
            BotFactory.create_bot_from_type(user_type = user_type,
                                            dbconn = self.mobile_dbconn)



if __name__ == '__main__':
    unittest.main()
