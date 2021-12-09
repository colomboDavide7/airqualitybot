######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import List
import airquality.filter.filter as basefilter
import airquality.types.timestamp as tstype
import airquality.types.apiresp.measresp as resptype


class TimestampFilter(basefilter.FilterABC):

    def __init__(self, log_filename="log"):
        super(TimestampFilter, self).__init__(log_filename=log_filename)
        self.filter_ts = tstype.NullTimestamp()

    def set_filter_ts(self, filter_ts: tstype.SQLTimestamp):
        self.filter_ts = filter_ts

    ################################ filter() ################################
    def filter(self, resp2filter: List[resptype.MeasureAPIResp]) -> List[resptype.MeasureAPIResp]:

        if not resp2filter:
            self.log_warning(f"{self.__class__.__name__} found empty responses => return")
            return resp2filter

        tot = len(resp2filter)
        first_timestamp = resp2filter[0].timestamp
        last_timestamp = resp2filter[-1].timestamp
        time_range_msg = f"[{first_timestamp.ts} - {last_timestamp.ts}]"

        if first_timestamp.is_after(last_timestamp):
            resp2filter.reverse()
            self.log_info(f"{self.__class__.__name__} found responses in descending order => reverse")

        if first_timestamp.is_after(self.filter_ts):
            self.log_info(f"{self.__class__.__name__} found {tot}/{tot} new measurements between {time_range_msg}")
            return resp2filter

        resp2filter = self.filter_out_old_measurements(resp2filter)
        self.log_info(f"{self.__class__.__name__} found {len(resp2filter)}/{tot} new measurements between {time_range_msg}")

        return resp2filter

    ################################ filter_out_old_measurements() ################################
    def filter_out_old_measurements(self, responses: List[resptype.MeasureAPIResp]) -> List[resptype.MeasureAPIResp]:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            if not responses[item_idx].timestamp.is_after(self.filter_ts):
                del responses[item_idx]
            else:
                item_idx = next(item_iter)
        return responses
