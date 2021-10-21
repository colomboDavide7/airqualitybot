#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 18:20
# @Description: test file for the Session class behaviour
#
#################################################

import unittest
from airquality.app.session import Session


class TestSession(unittest.TestCase):


    def test_new_session(self):
        """Test method for testing the creation of a new Session object"""

        # TEST 1 - test with all possible arguments
        test_args = {"debug": True, "logging": True}
        session = Session(test_args)
        self.assertTrue(session.debug)
        self.assertTrue(session.logging)

        # TEST 2 - test with no arguments
        test_args = {}
        session = Session(test_args)
        self.assertFalse(session.debug)
        self.assertFalse(session.logging)

        # TEST 3 - test with single argument
        test_args = {"debug": True}
        session = Session(test_args)
        self.assertTrue(session.debug)
        self.assertFalse(session.logging)

        test_args = {"logging": True}
        session = Session(test_args)
        self.assertFalse(session.debug)
        self.assertTrue(session.logging)


    def test_debug_message(self):
        """Test debug message method."""
        test_args = {"debug": True}
        session = Session(test_args)
        response = session.debug_msg("TEST DEBUG MESSAGE")
        self.assertTrue(response)

        test_args = {}
        session = Session(test_args)
        response = session.debug_msg("TEST DEBUG MESSAGE")
        self.assertFalse(response)



################################ EXECUTABLE ################################
if __name__ == '__main__':
    unittest.main()
