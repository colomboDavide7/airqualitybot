######################################################
#
# Author: Davide Colombo
# Date: 16/12/21 09:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.application import Application

if __name__ == '__main__':
    with Application() as runner:
        runner.main()
