#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 19:08
# @Description: Test script for testing the behaviour of the Bots
#
#################################################

import unittest
from airquality.bot.bot import BotMobile
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
        self.models = ["Atmotube Pro"]

    def test_create_bot_mobile(self):
        """Test the correct creation of the BotMobile instance."""
        bot = BotMobile(self.mobile_dbconn, self.models)
        self.assertIsNotNone(bot)
        self.assertIsInstance(bot, BotMobile)



if __name__ == '__main__':
    unittest.main()
