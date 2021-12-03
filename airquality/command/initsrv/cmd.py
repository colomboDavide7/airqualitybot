######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 16:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.logger.util.decorator as log_decorator
import airquality.command.basecmd as cmd


class ServiceInitCommand(cmd.Command):

    def __init__(self, log_filename="geonames"):
        super(ServiceInitCommand, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def execute(self):
        pass
        # geonames_country_files = [f for f in os.listdir(path=)]

        # for each file

        # 1 - select geographical area from country code

        # 2 - read the file content
        # 3 - parse the file content
        # 4 - build responses

        # 5 - apply filter

        # 6 - insert
