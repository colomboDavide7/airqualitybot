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
            log_filename="log"
    ):
        super(UpdateCommand, self).__init__(ub=ub, fw=fw, log_filename=log_filename)
        self.insert_wrapper = iw
        self.select_wrapper = sw
        self.api_resp_builder = arb

    # ************************************ execute ************************************
    @log_decorator.log_decorator()
    def execute(self):

        # Query database active locations
        db_responses = self.select_wrapper.select()
        if not db_responses:
            self.log_warning(f"{UpdateCommand.__name__}: empty database response => no location updated")
            return

        # Build url for fetching data from API
        url = self.url_builder.build()

        # Fetch API data
        parsed_response = self.fetch_wrapper.fetch(url=url)

        api_responses = self.api_resp_builder.build(parsed_resp=parsed_response)
        if not api_responses:
            self.log_warning(f"{UpdateCommand.__name__}: empty API response => no location updated")
            return

        # Create the Database Locations Dict
        database_active_locations = {}
        for dbresp in db_responses:
            database_active_locations[dbresp.sensor_name] = dbresp.geometry.as_text()

        # Create GeoFilter
        api_resp_filter = flt.GeoFilter(database_active_locations=database_active_locations, log_filename=self.log_filename)
        api_resp_filter.set_file_logger(self.file_logger)
        api_resp_filter.set_console_logger(self.console_logger)

        # Filter sensor data
        filtered_responses = api_resp_filter.filter(resp2filter=api_responses)
        if not filtered_responses:
            self.log_warning(f"{UpdateCommand.__name__}: all sensor locations are the same => no location updated")
            return

        # Insert new locations
        sensor_name2id = {r.sensor_name: r.sensor_id for r in db_responses}
        self.insert_wrapper.with_sensor_name2id(sensor_name2id)
        self.insert_wrapper.insert(filtered_responses)
