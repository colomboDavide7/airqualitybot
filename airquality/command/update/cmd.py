######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.logger.util.decorator as log_decorator
import airquality.command.basecmd as basecmd
import airquality.database.repo.geolocation as dbrepo
import airquality.filter.geolocation as geofilter
import airquality.source.api as apisource


class UpdateCommand(basecmd.Command):

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
        if not api_responses:
            self.log_warning(f"{UpdateCommand.__name__}: empty API response => no location updated")
            return

        filtered_responses = self.response_filter.filter(api_responses)
        if not filtered_responses:
            self.log_warning(f"{UpdateCommand.__name__}: all sensor locations are the same => no location updated")
            return

        self.db_repo.push(filtered_responses)
