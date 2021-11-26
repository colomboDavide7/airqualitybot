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
        self.filter_ts = None

    def set_filter_ts(self, filter_ts=ts.SQLTimestamp):
        self.filter_ts = filter_ts

    # ************************************ filter ************************************
    def filter(self, resp2filter: List[resp.MeasureAPIResp]) -> List[resp.MeasureAPIResp]:
        filtered_responses = []
        for response in resp2filter:
            if response.timestamp.is_after(self.filter_ts):
                filtered_responses.append(response)

        self.log_info(f"{TimestampFilter.__name__}: found {len(filtered_responses)}/{len(resp2filter)} new measurements")
        return filtered_responses
