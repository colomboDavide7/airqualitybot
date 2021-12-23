######################################################
#
# Author: Davide Colombo
# Date: 23/12/21 11:16
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import time
from unittest import TestCase, main
from airquality.program_timer import ProgramTimer


class TestProgramTimer(TestCase):

    def test_correct_usage(self):
        with ProgramTimer() as timer:
            time.sleep(0.01)
        self.assertGreater(timer.elapsed, 0)

    def test_ValueError_if_timer_is_not_started(self):
        timer = ProgramTimer()
        with self.assertRaises(ValueError):
            timer.elapsed

    def test_ValueError_if_timer_is_started_but_not_stopped(self):
        with ProgramTimer() as timer:
            with self.assertRaises(ValueError):
                timer.elapsed


if __name__ == '__main__':
    main()
