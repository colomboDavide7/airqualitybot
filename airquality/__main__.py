######################################################
#
# Author: Davide Colombo
# Date: 16/12/21 09:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.application import Application
from airquality.environment import Environment

if __name__ == '__main__':
    with Application(env=Environment()) as runner:
        runner.main()
