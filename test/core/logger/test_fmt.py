######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 13/11/21 16:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import logger.fmt as formt
import logger.log as log


class TestFormatter(unittest.TestCase):

    def test_get_formatter_class(self):
        obj_cls = formt.get_formatter_cls()
        self.assertEqual(obj_cls, formt.CustomFormatter)

        obj_cls = formt.get_formatter_cls(use_color=True)
        self.assertEqual(obj_cls, formt.ColoredFormatter)

    def test_get_handler_class(self):
        obj_cls = log.get_handler_cls(use_file=False)
        self.assertEqual(obj_cls, log.logging.StreamHandler)

        obj_cls = log.get_handler_cls(use_file=True)
        self.assertEqual(obj_cls, log.logging.FileHandler)


if __name__ == '__main__':
    unittest.main()
