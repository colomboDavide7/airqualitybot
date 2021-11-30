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
import airquality.api.url.purpurl as purl
import airquality.api.resp.info.purpleair as resp
import airquality.database.op.ins.geo as ins
import airquality.database.op.sel.info as sel
import airquality.filter.geofilt as flt


class UpdateCommand(basecmd.Command):

    def __init__(
            self,
            ub: purl.PurpleairURLBuilder,
            fw: apiwrp.FetchWrapper,
            iw: ins.GeoInsertWrapper,
            sw: sel.SensorInfoSelectWrapper,
            arb: resp.PurpleairAPIRespBuilder,
            rf: flt.GeoFilter,
            log_filename="log"
    ):
        super(UpdateCommand, self).__init__(ub=ub, fw=fw, log_filename=log_filename)
        self.insert_wrapper = iw
        self.select_wrapper = sw
        self.api_resp_builder = arb
        self.response_filter = rf

    # ************************************ execute ************************************
    @log_decorator.log_decorator()
    def execute(self):

        # Query database sensors
        db_responses = self.select_wrapper.select()
        if not db_responses:
            self.log_warning(f"{UpdateCommand.__name__}: empty database response => no location updated")
            return

        # Fetch API data
        url = self.url_builder.build()
        parsed_response = self.fetch_wrapper.fetch(url=url)
        api_responses = self.api_resp_builder.build(parsed_resp=parsed_response)
        if not api_responses:
            self.log_warning(f"{UpdateCommand.__name__}: empty API response => no location updated")
            return

        # Filter locations
        self.response_filter.with_database_locations({r.sensor_name: r.geometry.as_text() for r in db_responses})
        filtered_responses = self.response_filter.filter(resp2filter=api_responses)
        if not filtered_responses:
            self.log_warning(f"{UpdateCommand.__name__}: all sensor locations are the same => no location updated")
            return

        # Insert new locations
        sensor_name2id = {r.sensor_name: r.sensor_id for r in db_responses}
        self.insert_wrapper.with_sensor_name2id(sensor_name2id)
        self.insert_wrapper.insert(filtered_responses)
