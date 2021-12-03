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
import airquality.database.op.ins.info as ins
import airquality.database.op.sel.info as sel


class InitCommand(basecmd.Command):

    def __init__(
            self,
            ub: purl.PurpleairURLBuilder,
            fw: apiwrp.FetchWrapper,
            iw: ins.InfoInsertWrapper,
            sw: sel.SensorInfoSelectWrapper,
            arb: resp.PurpleairAPIRespBuilder,
            flt: nameflt.NameFilter,
            log_filename="log"
    ):
        super(InitCommand, self).__init__(log_filename=log_filename)
        self.insert_wrapper = iw
        self.select_wrapper = sw
        self.api_resp_builder = arb
        self.response_filter = flt
        self.url_builder = ub
        self.fetch_wrapper = fw

    @log_decorator.log_decorator()
    def execute(self):

        ################################ API-SIDE ###############################
        # Build the URL
        url = self.url_builder.build()

        parsed_response = self.fetch_wrapper.fetch(url=url)

        api_responses = self.api_resp_builder.build(parsed_resp=parsed_response)
        if not api_responses:
            self.log_warning(f"{InitCommand.__name__}: empty API sensor data => no sensor inserted")
            return

        # Select sensor data from the database
        db_responses = self.select_wrapper.select()

        # If there are any existing sensor within the database
        if db_responses:

            self.response_filter.with_database_sensor_names(dbnames=[r.sensor_name for r in db_responses])
            filtered_responses = self.response_filter.filter(resp2filter=api_responses)
            if not filtered_responses:
                self.log_warning(
                    f"{InitCommand.__name__}: all sensors are already present into the database => no sensor inserted")
                return

            # update the api responses with the filtered ones
            api_responses = filtered_responses

        ################################ DATABASE-SIDE ###############################
        max_sensor_id = self.select_wrapper.select_max_sensor_id()
        self.insert_wrapper.with_start_insert_sensor_id(max_sensor_id)
        self.insert_wrapper.insert(api_responses)
