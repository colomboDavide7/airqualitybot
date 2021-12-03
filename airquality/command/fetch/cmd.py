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
import airquality.api.resp.measure.measure as resp
import airquality.api.url.dynurl as url
import airquality.api.url.timedecor as urldec
import airquality.database.op.ins.measure as ins
import airquality.database.op.sel.measure as sel
import airquality.filter.tsfilt as filt
import airquality.types.timestamp as ts


class FetchCommand(base.Command):

    ################################ __init__ ###############################
    def __init__(
            self,
            tud: urldec.URLTimeDecorator,
            ub: url.DynamicURLBuilder,
            arb: resp.MeasureAPIRespBuilder,
            fw: apiwrp.FetchWrapper,
            iw: ins.MeasureInsertWrapper,
            sw: sel.MeasureSelectWrapper,
            flt: filt.TimestampFilter,
            log_filename="log"
    ):
        super(FetchCommand, self).__init__(log_filename=log_filename)
        self.insert_wrapper = iw
        self.select_wrapper = sw
        self.time_url_decorator = tud
        self.time_filter = flt
        self.api_resp_builder = arb
        self.url_builder = ub
        self.fetch_wrapper = fw

    ################################ execute ###############################
    @log_decorator.log_decorator()
    def execute(self):

        db_responses = self.select_wrapper.select()
        if not db_responses:
            self.log_warning(f"{FetchCommand.__name__}: no sensor found inside the database => no measure inserted")
            return

        for dbresp in db_responses:
            for channel in dbresp.api_param:

                last_acquisition = channel.last_acquisition
                self.time_filter.set_filter_ts(last_acquisition)

                self.time_url_decorator.can_start_again().from_(last_acquisition).to_(ts.CurrentTimestamp())
                self.time_url_decorator.with_identifier(channel.ch_id).with_api_key(channel.ch_key)

                while self.time_url_decorator.has_next_date():
                    next_url = self.time_url_decorator.build()
                    parsed_response = self.fetch_wrapper.fetch(next_url)
                    api_responses = self.api_resp_builder.with_channel_name(channel.ch_name).build(parsed_response)
                    if not api_responses:
                        self.log_warning(f"{FetchCommand.__name__}: empty API response => skip to next date")
                        continue

                    filtered_responses = self.time_filter.filter(api_responses)
                    if not filtered_responses:
                        self.log_warning(f"{FetchCommand.__name__}: no new measurements => skip to next date")
                        continue

                    # Database insertion
                    max_record_id = self.select_wrapper.select_max_record_id()
                    name2id = self.select_wrapper.select_measure_param()

                    self.insert_wrapper\
                        .with_sensor_id(dbresp.sensor_id)\
                        .with_measure_param_name2id(name2id)\
                        .with_start_insert_record_id(max_record_id)\
                        .with_channel_name(channel.ch_name)

                    self.insert_wrapper.insert(filtered_responses)
