######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 11:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.logger.util.decorator as log_decorator
import airquality.command.basecmd as basecmd
import airquality.filter.namefilt as nameflt
import airquality.database.repo.info as dbrepo
import api as apisource


class InitCommand(basecmd.Command):

    def __init__(
            self,
            api_source: apisource.APISourceABC,
            db_repo: dbrepo.SensorInfoRepository,
            response_filter: nameflt.NameFilter,
            log_filename="log"
    ):
        super(InitCommand, self).__init__(log_filename=log_filename)
        self.api_source = api_source
        self.db_repo = db_repo
        self.response_filter = response_filter

    @log_decorator.log_decorator()
    def execute(self):
        api_responses = self.api_source.get()
        filtered_responses = self.response_filter.filter(api_responses)
        self.db_repo.push(filtered_responses)
