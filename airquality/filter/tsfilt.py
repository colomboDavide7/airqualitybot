######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.filter.basefilt as base
import airquality.adapter.api2db.fetchadpt.fetchadpt as ftchadpt
import airquality.database.util.datatype.timestamp as ts


class TimestampFilter(base.BaseFilter):

    def __init__(self, log_filename="log"):
        super(TimestampFilter, self).__init__(log_filename=log_filename)
        self.filter_ts = None

    def set_filter_ts(self, filter_ts=ts.SQLTimestamp):
        self.filter_ts = filter_ts

    def filter(self, to_filter: List[ftchadpt.FetchUniformModel]) -> List[ftchadpt.FetchUniformModel]:
        filtered_data = []
        for data in to_filter:
            if data.timestamp.is_after(self.filter_ts):
                filtered_data.append(data)

        self.log_info(f"{TimestampFilter.__name__}: found {len(filtered_data)}/{len(to_filter)} new measurements")
        return filtered_data
