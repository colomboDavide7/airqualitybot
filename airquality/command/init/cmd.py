######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 11:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.logger.util.decorator as log_decorator
import airquality.command.basecmd as basecmd
import airquality.api.fetchwrp as apiwrp
import airquality.api.url.purpurl as purl
import airquality.api.resp.info.purpleair as resp
import airquality.filter.namefilt as nameflt
import airquality.database.repo.info_repo as dbrepo


class InitCommand(basecmd.Command):

    def __init__(
            self,
            ub: purl.PurpleairURLBuilder,
            fw: apiwrp.FetchWrapper,
            repo: dbrepo.SensorInfoRepository,
            arb: resp.PurpleairAPIRespBuilder,
            flt: nameflt.NameFilter,
            log_filename="log"
    ):
        super(InitCommand, self).__init__(log_filename=log_filename)
        self.repo = repo
        self.api_resp_builder = arb
        self.response_filter = flt
        self.url_builder = ub
        self.fetch_wrapper = fw

    @log_decorator.log_decorator()
    def execute(self):

        url = self.url_builder.build()
        parsed_response = self.fetch_wrapper.fetch(url=url)
        api_responses = self.api_resp_builder.build(parsed_resp=parsed_response)
        if not api_responses:
            self.log_warning(f"{InitCommand.__name__}: empty API sensor data => no sensor inserted")
            return

        filtered_responses = self.response_filter.filter(api_responses)
        if not filtered_responses:
            self.log_warning(
                f"{InitCommand.__name__}: all sensors are already present into the database => no sensor inserted")
            return

        self.repo.push(filtered_responses)
