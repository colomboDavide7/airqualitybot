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

        # TEST 1 - test with full dictionary
        test_args = {"debug": True, "logging": True}
        session = Session(**test_args)
        self.assertTrue(session.is_debug_active())
        self.assertTrue(session.is_logging_active())

        # TEST 2 - test with empty args dictionary
        test_args = {}
        session = Session(**test_args)
        self.assertFalse(session.is_debug_active())
        self.assertFalse(session.is_logging_active())

        # TEST 3 - test with mixed dictionary
        test_args = {"debug": True}
        session = Session(**test_args)
        self.assertTrue(session.is_debug_active())
        self.assertFalse(session.is_logging_active())

        test_args = {"logging": True}
        session = Session(**test_args)
        self.assertFalse(session.is_debug_active())
        self.assertTrue(session.is_logging_active())


################################ EXECUTABLE ################################
if __name__ == '__main__':
    unittest.main()
