######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.logger.util.decorator as log_decorator
import airquality.command.basecmd as basecmd
import airquality.api.fetchwrp as apiwrp
import airquality.api.url.public as purl
import airquality.api.resp.info.purpleair as resp
import airquality.database.repo.geo as dbrepo
import airquality.filter.geofilt as flt


class UpdateCommand(basecmd.Command):

    def __init__(
            self,
            ub: purl.PurpleairURLBuilder,
            fw: apiwrp.FetchWrapper,
            repo: dbrepo.SensorGeoRepository,
            arb: resp.PurpleairAPIRespBuilder,
            rf: flt.GeoFilter,
            log_filename="log"
    ):
        super(UpdateCommand, self).__init__(log_filename=log_filename)
        self.repo = repo
        self.api_resp_builder = arb
        self.response_filter = rf
        self.url_builder = ub
        self.fetch_wrapper = fw

    # ************************************ execute ************************************
    @log_decorator.log_decorator()
    def execute(self):

        url = self.url_builder.build()
        parsed_response = self.fetch_wrapper.fetch(url=url)
        api_responses = self.api_resp_builder.build(parsed_resp=parsed_response)
        if not api_responses:
            self.log_warning(f"{UpdateCommand.__name__}: empty API response => no location updated")
            return

        filtered_responses = self.response_filter.filter(api_responses)
        if not filtered_responses:
            self.log_warning(f"{UpdateCommand.__name__}: all sensor locations are the same => no location updated")
            return

        self.repo.push(filtered_responses)
