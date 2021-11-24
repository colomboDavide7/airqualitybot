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
import airquality.api2db.updtunif.updtunif as unif
import airquality.database.op.ins.updtins as ins
import airquality.database.op.sel.stationsel as sel
import airquality.database.rec.updtrec as rec
import airquality.filter.geofilt as flt


class UpdateCommand(basecmd.Command):

    def __init__(
            self,
            fw: apiwrp.FetchWrapper,
            iw: ins.UpdateInsertWrapper,
            sw: sel.StationSelectWrapper,
            urb: unif.UpdateUniformResponseBuilder,
            rb: rec.UpdateRecordBuilder,
            log_filename="purpleair"
    ):
        super(UpdateCommand, self).__init__(fw=fw, iw=iw, log_filename=log_filename)
        self.uniform_response_builder = urb
        self.record_builder = rb
        self.select_wrapper = sw

    # ************************************ execute ************************************
    @log_decorator.log_decorator()
    def execute(self):

        # Query database active locations
        db_responses = self.select_wrapper.select()
        if not db_responses:
            self.log_warning(f"{UpdateCommand.__name__}: empty database response => no location updated")
            return

        # Fetch API data
        api_responses = self.fetch_wrapper.fetch()
        if not api_responses:
            self.log_warning(f"{UpdateCommand.__name__}: empty API response => no location updated")
            return

        # Reshape API data
        uniformed_responses = self.uniform_response_builder.uniform(responses=api_responses)

        # Create the Database Locations Dict
        database_active_locations = {}
        for resp in db_responses:
            database_active_locations[resp.sensor_name] = resp.geometry.as_text()

        # Create GeoFilter
        uniform_resp_filter = flt.GeoFilter(database_active_locations=database_active_locations, log_filename=self.log_filename)
        uniform_resp_filter.set_file_logger(self.file_logger)
        uniform_resp_filter.set_console_logger(self.console_logger)

        # Filter sensor data
        filtered_responses = uniform_resp_filter.filter(resp2filter=uniformed_responses)
        if not filtered_responses:
            self.log_warning(f"{UpdateCommand.__name__}: all sensor locations are the same => no location updated")
            return

        # Create sensor_name - sensor_id map
        name_id_map = {}
        for resp in db_responses:
            name_id_map[resp.sensor_name] = resp.sensor_id

        # Build database records
        records = []
        for api_resp in filtered_responses:

            records.append(self.record_builder.record(api_resp, sensor_id=name_id_map[api_resp.sensor_name]))

        # Update locations
        self.insert_wrapper.insert(records=records)
