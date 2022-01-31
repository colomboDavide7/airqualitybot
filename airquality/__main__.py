######################################################
#
# Author: Davide Colombo
# Date: 16/12/21 09:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

# LOGGING MODULE CONFIGURATION

# this must be done before importing any other
# module within the program, otherwise loggers
# won't work.

import json
import logging.config

with open('./logger_conf.json', 'r') as fconf:
    logging.config.dictConfig(json.load(fconf))

######################################################
from airquality.application import Application


if __name__ == '__main__':
    with Application() as runner:
        runner.main()
