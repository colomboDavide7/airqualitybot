######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.filter.abc as basefilter
import airquality.types.timest as tstype
import airquality.api.resp.abc as resptype

RESPONSE_TYPE = List[resptype.MeasureAPIRespTypeABC]


# ------------------------------- TimestFilter ------------------------------- #
class TimestFilter(basefilter.FilterABC):

    def __init__(self, timest_boundary: tstype.TimestABC):
        super(TimestFilter, self).__init__()
        self.timest_boundary = timest_boundary

    ################################ filter() ################################
    def filter(self, all_resp: RESPONSE_TYPE) -> RESPONSE_TYPE:
        tot = len(all_resp)
        first_timest = all_resp[0].measured_at()
        last_timest = all_resp[-1].measured_at()
        time_range_str = f"[{first_timest.ts} - {last_timest.ts}]"

        if first_timest.is_after(last_timest):
            self.log_info(f"{self.__class__.__name__} found responses in descending order => reverse")
            all_resp.reverse()

        if first_timest.is_after(self.timest_boundary):
            self.log_info(f"{self.__class__.__name__} found {tot}/{tot} new measurements between {time_range_str}")
            return all_resp

        all_resp = self.purge_responses_before_or_equal_to_timest_boundary(all_resp)
        self.log_info(f"{self.__class__.__name__} found {len(all_resp)}/{tot} new measurements between {time_range_str}")

        return all_resp

    ############################### purge_responses_before_or_equal_to_timest_boundary() ###############################
    def purge_responses_before_or_equal_to_timest_boundary(self, responses: RESPONSE_TYPE) -> RESPONSE_TYPE:
        last_idx_to_del = 0
        for idx, response in enumerate(responses):
            if not response.measured_at().is_after(self.timest_boundary):
                last_idx_to_del = idx

        del responses[:last_idx_to_del+1]
        return responses
