######################################################
#
# Author: Davide Colombo
# Date: 16/12/21 09:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import json
import logging.config
from airquality.application import Application

if __name__ == '__main__':
    with open('./logger_conf.json', 'r') as fconf:
        logging.config.dictConfig(json.load(fconf))

    with Application() as runner:
        runner.main()
