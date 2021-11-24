######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 19:49
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.looper.datelooper as dtloop
import airquality.logger.util.decorator as log_decorator
import airquality.database.dtype.timestamp as ts
import airquality.api.fetchwrp as apiwrp
import airquality.api.resp.baseresp as baseresp


class AtmotubeDateLooper(dtloop.DateLooper):

    def __init__(self, fetch_wrapper: apiwrp.FetchWrapper, start_ts: ts.SQLTimestamp, stop_ts: ts.SQLTimestamp, log_filename="app"):
        super(AtmotubeDateLooper, self).__init__(fetch_wrapper=fetch_wrapper, log_filename=log_filename)
        self.start = start_ts
        self.stop = stop_ts
        self.ended = False

    def has_next(self):
        return not self.ended

    @log_decorator.log_decorator()
    def get_next_sensor_data(self) -> List[baseresp.BaseResponse]:
        next_date = self._get_next_date_url_param()
        self.log_info(f"{AtmotubeDateLooper.__name__}: looking for new sensor data on date='{next_date['date']}'")
        self.fetch_wrapper.add_database_api_param(next_date)
        return self.fetch_wrapper.fetch()

    def _get_next_date_url_param(self) -> Dict[str, Any]:
        date = self.start
        if date.is_after(self.stop) or date.is_same_day(self.stop):
            self.ended = True
            date = self.stop
        self.start = self.start.add_days(1)
        return {'date': date.ts.split(' ')[0]}
