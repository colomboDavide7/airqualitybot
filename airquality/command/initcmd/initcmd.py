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
import airquality.api2db.initunif.initunif as initunif
import airquality.filter.namefilt as nameflt
import airquality.database.rec.initrec as initrec
import airquality.database.op.ins.initins as ins
import airquality.database.op.sel.stationsel as sel


class InitCommand(basecmd.Command):

    def __init__(
            self, fw: apiwrp.FetchWrapper, urb: initunif.InitUniformResponseBuilder, rb: initrec.InitRecordBuilder,
            iw: ins.InitInsertWrapper, sw: sel.StationSelectWrapper, log_filename="log"
    ):
        super(InitCommand, self).__init__(fw=fw, iw=iw, log_filename=log_filename)
        self.uniform_response_builder = urb
        self.record_builder = rb
        self.select_wrapper = sw

    @log_decorator.log_decorator()
    def execute(self):

        ################################ API-SIDE ###############################
        api_responses = self.fetch_wrapper.fetch()
        if not api_responses:
            self.log_warning(f"{InitCommand.__name__}: empty API sensor data => no sensor inserted")
            return

        ####################### UNIFORM API RESPONSES TO APPLY ANY USEFUL INTERMEDIATE OPERATION #######################
        uniformed_responses = self.uniform_response_builder.uniform(api_responses)

        ################################ FILTERING OPERATION ###############################
        db_responses = self.select_wrapper.select()

        if db_responses:
            database_sensor_names = []
            for resp in db_responses:
                database_sensor_names.append(resp.sensor_name)
            uniform_response_filter = nameflt.NameFilter(database_sensor_names=database_sensor_names, log_filename=self.log_filename)
            uniform_response_filter.set_file_logger(self.file_logger)
            uniform_response_filter.set_console_logger(self.console_logger)

            filtered_responses = uniform_response_filter.filter(resp2filter=uniformed_responses)
            if not filtered_responses:
                self.log_warning(f"{InitCommand.__name__}: all sensors are already present into the database => no sensor inserted")
                return

            uniformed_responses = filtered_responses

        ################################ DATABASE-SIDE ###############################
        max_sensor_id = self.select_wrapper.select_max_sensor_id()
        self.log_info(f"{InitCommand.__name__}: new insertion starts at sensor_id={max_sensor_id}")

        records = []
        for response in uniformed_responses:
            records.append(
                self.record_builder.record(uniform_response=response, sensor_id=max_sensor_id)
            )
            max_sensor_id += 1

        # Execute queries on sensors
        self.insert_wrapper.insert(records=records)
