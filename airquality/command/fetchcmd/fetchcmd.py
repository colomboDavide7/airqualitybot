######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 17:49
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.command.basecmd as base
import airquality.logger.util.decorator as log_decorator
import airquality.api.fetchwrp as apiwrp
import airquality.api.resp.measure as resp
import airquality.api.url.dynurl as url
import airquality.api.url.timedecor as urldec
import airquality.database.op.ins.measure as ins
import airquality.database.op.sel.measure as sel
import airquality.database.rec.measure as rec
import airquality.filter.tsfilt as filt
import airquality.types.timestamp as ts


class FetchCommand(base.Command):

    ################################ __init__ ###############################
    def __init__(
            self,
            tud: urldec.URLTimeDecorator,
            ub: url.DynamicURLBuilder,
            arb: resp.MeasureBuilder,
            fw: apiwrp.FetchWrapper,
            iw: ins.MeasureInsertWrapper,
            sw: sel.MeasureSelectWrapper,
            flt: filt.TimestampFilter,
            rb_cls=rec.MeasureRecord,
            log_filename="log"
    ):
        super(FetchCommand, self).__init__(ub=ub, fw=fw, log_filename=log_filename)
        self.insert_wrapper = iw
        self.select_wrapper = sw
        self.record_class = rb_cls
        self.time_url_decorator = tud
        self.time_filter = flt
        self.api_resp_builder = arb

    ################################ execute ###############################
    @log_decorator.log_decorator()
    def execute(self):

        # Query sensor ids from database
        db_responses = self.select_wrapper.select()
        if not db_responses:
            self.log_warning(f"{FetchCommand.__name__}: no sensor found inside the database => no measure inserted")
            return

        for dbresp in db_responses:
            for channel in dbresp.api_param:

                last_acquisition = channel.last_acquisition
                self.log_info(f"{FetchCommand.__name__}: last acquisition => {last_acquisition.get_formatted_timestamp()}")

                # Set start and stop time range
                self.time_url_decorator.with_start_ts(start=last_acquisition).with_stop_ts(ts.CurrentTimestamp())

                # Update the decorated URL identifier and api key
                self.time_url_decorator.url_to_decorate.with_identifier(channel.ch_id).with_api_key(channel.ch_key)
                self.time_url_decorator.ended = False

                while self.time_url_decorator.has_next_date():

                    # Fetch API data
                    parsed_response = self.fetch_wrapper.fetch(url=self.time_url_decorator.build())

                    # Build the API responses
                    api_responses = self.api_resp_builder\
                        .with_channel_name(channel_name=channel.ch_name)\
                        .build(parsed_resp=parsed_response)

                    if not api_responses:
                        self.log_warning(f"{FetchCommand.__name__}: empty API response => skip to next date")
                        continue

                    if last_acquisition.is_after(api_responses[0].timestamp):
                        # Set filter timestamp
                        self.time_filter.set_filter_ts(last_acquisition)

                        # Filter responses
                        filtered_responses = self.time_filter.filter(api_responses)

                        if not filtered_responses:
                            self.log_warning(f"{FetchCommand.__name__}: no new measurements => skip to next date")
                            continue

                        # update the api responses memory reference
                        api_responses = filtered_responses

                    # Build record
                    max_record_id = self.select_wrapper.select_max_record_id()
                    self.log_info(f"{FetchCommand.__name__}: new insertion starts at => {max_record_id}")

                    # Measure param
                    name2id = self.select_wrapper.select_measure_param()

                    records = []
                    for api_resp in api_responses:
                        records.append(
                            self.record_class(record_id=max_record_id, name2id=name2id, response=api_resp)
                        )
                        max_record_id += 1

                    # Insert measurements
                    self.insert_wrapper.concat_measure_query(records=records)

                    current_last_acquisition = records[-1].response.timestamp.get_formatted_timestamp()
                    self.insert_wrapper.concat_update_last_acquisition_timestamp_query(
                        sensor_id=dbresp.sensor_id,
                        channel_name=channel.ch_name,
                        last_acquisition=current_last_acquisition
                    )
                    
                    
                    
                    

                    self.insert_wrapper.insert()
