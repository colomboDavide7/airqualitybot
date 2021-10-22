#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 18:20
# @Description: unit test script
#
#################################################

import unittest
from airquality.runner import set_session


class TestSession(unittest.TestCase):

    def setUp(self) -> None:
        self.session = set_session({})

    def test_new_session_debug_and_logging(self):
        """Test method for testing the creation of a new Session object"""
        self.session = set_session({"debug": True, "logging": True})
        self.assertTrue(self.session.debug)
        self.assertTrue(self.session.logging)

    def test_debug_message(self):
        """Test debug message method."""
        self.session = set_session({"debug": True})
        response = self.session.debug_msg("TEST DEBUG MESSAGE")
        self.assertTrue(response)

    def test_do_not_debug_msg_when_debug_false(self):
        response = self.session.debug_msg("TEST DEBUG MESSAGE")
        self.assertFalse(response)


################################ EXECUTABLE ################################
if __name__ == '__main__':
    unittest.main()
