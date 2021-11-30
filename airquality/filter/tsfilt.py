######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.filter.basefilt as base
import airquality.types.timestamp as ts
import airquality.types.apiresp.measresp as resp


class TimestampFilter(base.BaseFilter):

    def __init__(self, log_filename="log"):
        super(TimestampFilter, self).__init__(log_filename=log_filename)
        self.filter_ts = ts.NullTimestamp()

    def set_filter_ts(self, filter_ts=ts.SQLTimestamp):
        self.filter_ts = filter_ts

    def filter(self, resp2filter: List[resp.MeasureAPIResp]) -> List[resp.MeasureAPIResp]:
        all_responses = len(resp2filter)

        if not resp2filter[-1].timestamp.is_after(resp2filter[0].timestamp):
            self.log_info(f"{TimestampFilter.__name__}: api responses are in descending order => reverse")
            resp2filter.reverse()

        if resp2filter[0].timestamp.is_after(self.filter_ts):
            self.log_info(f"{TimestampFilter.__name__}: found {all_responses}/{all_responses} new measurements")
            return resp2filter

        count = 0
        item_idx = 0
        while count < all_responses:
            count += 1
            if not resp2filter[item_idx].timestamp.is_after(self.filter_ts):
                del resp2filter[item_idx]
            else:
                item_idx += 1

        self.log_info(f"{TimestampFilter.__name__}: found {len(resp2filter)}/{all_responses} new measurements")
        return resp2filter
