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
import airquality.api.resp.info as resp
import airquality.filter.namefilt as nameflt
import airquality.database.op.ins.info as ins
import airquality.database.op.sel.info as sel
import airquality.database.rec.info as rec


class InitCommand(basecmd.Command):

    def __init__(
            self,
            ub: purl.PurpleairURLBuilder,
            fw: apiwrp.FetchWrapper,
            iw: ins.StationInfoInsertWrapper,
            sw: sel.SensorInfoSelectWrapper,
            arb: resp.PurpleairSensorInfoBuilder,
            log_filename="log",
            rb_cls=rec.SensorInfoRecord
    ):
        super(InitCommand, self).__init__(ub=ub, fw=fw, log_filename=log_filename)
        self.insert_wrapper = iw
        self.select_wrapper = sw
        self.record_builder_cls = rb_cls
        self.api_resp_builder = arb

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
            database_sensor_names = []

            for dbresp in db_responses:
                database_sensor_names.append(dbresp.sensor_name)

            # Apply a filter for filtering out all the sensors that are already present into the database
            api_resp_filter = nameflt.NameFilter(database_sensor_names=database_sensor_names, log_filename=self.log_filename)
            api_resp_filter.set_file_logger(self.file_logger)
            api_resp_filter.set_console_logger(self.console_logger)

            filtered_responses = api_resp_filter.filter(resp2filter=api_responses)
            if not filtered_responses:
                self.log_warning(f"{InitCommand.__name__}: all sensors are already present into the database => no sensor inserted")
                return

            # update the api responses with the filtered ones
            api_responses = filtered_responses

        ################################ DATABASE-SIDE ###############################
        max_sensor_id = self.select_wrapper.select_max_sensor_id()
        self.log_info(f"{InitCommand.__name__}: new insertion starts at sensor_id={max_sensor_id}")

        records = []
        for response in api_responses:
            records.append(self.record_builder_cls(sensor_id=max_sensor_id, info_resp=response))
            max_sensor_id += 1

        # Concatenate all the queries and then execute once all of them
        self.insert_wrapper.concat_initialize_sensor_query(records=records)
        self.insert_wrapper.insert()
