######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 19:49
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
# from typing import List, Dict, Any
# import airquality.logger.util.decorator as log_decorator
# import airquality.database.dtype.timestamp as ts
# import airquality.api.fetchwrp as apiwrp
# import airquality.api.resp.resp as resp


# class ThingspeakDateLooper(dtloop.DateLooper):
#
#     def __init__(self, fw: apiwrp.FetchWrapper, strt: ts.SQLTimestamp, stp: ts.SQLTimestamp, log_filename="log"):
#         super(ThingspeakDateLooper, self).__init__(fw=fw, strt=strt, stp=stp, log_filename=log_filename)
#
#     def has_next(self):
#         return not self.ended
#
#     @log_decorator.log_decorator()
#     def get_next_api_responses(self) -> List[resp.APIResp]:
#         next_time_window = self._get_next_date_url_param()
#         self.log_info(f"{ThingspeakDateLooper.__name__}: looking for new measurements within date range "
#                       f"[{next_time_window['start']} - {next_time_window['end']}]")
#         self.fetch_wrapper.update_url_param(next_time_window)
#         return self.fetch_wrapper.fetch()
#
#     def _get_next_date_url_param(self) -> Dict[str, Any]:
#         date = self.start
#         end = self.start.add_days(7)
#         if end.is_after(self.stop) or end.is_same_day(self.stop):
#             self.ended = True
#             end = self.stop
#         self.start = self.start.add_days(7)
#         return {'start': date.ts, 'end': end.ts}
