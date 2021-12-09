######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import List
import airquality.filter.filter as base
import airquality.types.timestamp as ts
import airquality.types.apiresp.measresp as resp


class TimestampFilter(base.FilterABC):

    def __init__(self, log_filename="log"):
        super(TimestampFilter, self).__init__(log_filename=log_filename)
        self.filter_ts = ts.NullTimestamp()

    def set_filter_ts(self, filter_ts: ts.SQLTimestamp):
        self.filter_ts = filter_ts

    ################################ filter() ################################
    def filter(self, resp2filter: List[resp.MeasureAPIResp]) -> List[resp.MeasureAPIResp]:

        if not resp2filter:
            self.log_warning(f"{self.__class__.__name__} cannot apply filter to empty list => skip")
            return resp2filter

        all_responses = len(resp2filter)
        first_timestamp = resp2filter[0].timestamp
        last_timestamp = resp2filter[-1].timestamp

        if first_timestamp.is_after(last_timestamp):
            resp2filter.reverse()
        if first_timestamp.is_after(self.filter_ts):
            self.log_info(f"{self.__class__.__name__} found {all_responses}/{all_responses} new measurements between"
                          f"[{first_timestamp.ts} - {last_timestamp.ts}]")
            return resp2filter
        resp2filter = self.filter_out_old_measurements(resp2filter)

        self.log_info(f"{self.__class__.__name__} found {len(resp2filter)}/{all_responses} new measurements")
        return resp2filter

    ################################ filter_out_old_measurements() ################################
    def filter_out_old_measurements(self, responses: List[resp.MeasureAPIResp]) -> List[resp.MeasureAPIResp]:
        all_responses = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < all_responses:
            if not responses[item_idx].timestamp.is_after(self.filter_ts):
                del responses[item_idx]
            else:
                item_idx = next(item_iter)
        return responses
