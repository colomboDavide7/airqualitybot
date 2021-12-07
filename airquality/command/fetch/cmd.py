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
import airquality.api.url.timeiter as url
import airquality.database.repo.measure as dbrepo
import airquality.filter.tsfilt as filt
import airquality.types.timestamp as ts


class FetchCommand(base.Command):

    ################################ __init__ ###############################
    def __init__(
            self,
            time_iterable_url: url.TimeIterableURL,
            arb: resp.MeasureAPIRespBuilder,
            fw: apiwrp.FetchWrapper,
            repo: dbrepo.SensorMeasureRepoABC,
            flt: filt.TimestampFilter,
            log_filename="log"
    ):
        super(FetchCommand, self).__init__(log_filename=log_filename)
        self.repo = repo
        self.time_iterable_url = time_iterable_url
        self.time_filter = flt
        self.api_resp_builder = arb
        self.fetch_wrapper = fw

    ################################ execute ###############################
    @log_decorator.log_decorator()
    def execute(self):

        db_lookup = self.repo.lookup()
        if not db_lookup:
            self.log_warning(f"{FetchCommand.__name__}: no sensor found inside the database => no measure inserted")
            return

        for single_lookup in db_lookup:
            for ch in single_lookup.channels:

                last_acquisition = ch.last_acquisition
                self.time_filter.set_filter_ts(last_acquisition)

                self.time_iterable_url.from_(last_acquisition).to_(ts.CurrentTimestamp()).with_identifier(ch.ch_id).with_api_key(ch.ch_key)

                for url_item in self.time_iterable_url.build():
                    parsed_response = self.fetch_wrapper.fetch(url_item)
                    api_responses = self.api_resp_builder.with_channel_name(ch.ch_name).build(parsed_response)
                    if not api_responses:
                        self.log_warning(f"{FetchCommand.__name__}: empty API response => skip to next date")
                        continue

                    filtered_responses = self.time_filter.filter(api_responses)
                    if not filtered_responses:
                        self.log_warning(f"{FetchCommand.__name__}: no new measurements => skip to next date")
                        continue

                    self.repo.push_to(sensor_id=single_lookup.sensor_id, channel_name=ch.ch_name).push(filtered_responses)
