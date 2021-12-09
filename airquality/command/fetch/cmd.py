######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 17:49
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.command.basecmd as base
import airquality.logger.util.decorator as log_decorator
import airquality.database.repo.measure as dbrepo
import airquality.filter.tsfilt as filt
import airquality.source.api as apisource


class FetchCommand(base.Command):

    ################################ __init__ ###############################
    def __init__(
            self,
            api_source: apisource.APISourceABC,
            db_repo: dbrepo.SensorMeasureRepoABC,
            response_filter: filt.TimestampFilter,
            log_filename="log"
    ):
        super(FetchCommand, self).__init__(log_filename=log_filename)
        self.db_repo = db_repo
        self.api_source = api_source
        self.time_filter = response_filter

    @log_decorator.log_decorator()
    def execute(self):
        api_responses = self.api_source.get()
        for response in api_responses:
            filtered_responses = self.time_filter.filter(response)
            self.db_repo.push(filtered_responses)
