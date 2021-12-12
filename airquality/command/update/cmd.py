######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.logger.util.decorator as log_decorator
import airquality.command.abc as basecmd
import airquality.database.repo.geolocation as dbrepo
import airquality.filter.geolocation as geofilter
import api as apisource


class UpdateCommand(basecmd.CommandABC):

    def __init__(
            self,
            api_source: apisource.APISourceABC,
            db_repo: dbrepo.SensorGeoRepository,
            response_filter: geofilter.GeoFilter,
            log_filename="log"
    ):
        super(UpdateCommand, self).__init__(log_filename=log_filename)
        self.api_source = api_source
        self.db_repo = db_repo
        self.response_filter = response_filter

    @log_decorator.log_decorator()
    def execute(self):
        api_responses = self.api_source.get()
        filtered_responses = self.response_filter.filter(api_responses)
        self.db_repo.push(filtered_responses)
