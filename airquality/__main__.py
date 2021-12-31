######################################################
#
# Author: Davide Colombo
# Date: 16/12/21 09:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.runner import Runner
from airquality.environment import Environment

if __name__ == '__main__':
    with Runner(env=Environment()) as runner:
        runner.main()
