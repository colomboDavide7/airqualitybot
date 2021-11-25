######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 16:40
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.logger.loggable as log
import airquality.api.fetchwrp as apiwrp
import airquality.database.dtype.timestamp as ts
import airquality.api.resp.resp as resp


class DateLooper(log.Loggable):

    def __init__(self, fw: apiwrp.FetchWrapper, strt: ts.SQLTimestamp, stp: ts.SQLTimestamp, log_filename="log"):
        super(DateLooper, self).__init__(log_filename=log_filename)
        self.fetch_wrapper = fw
        self.start = strt
        self.stop = stp
        self.ended = False

    @abc.abstractmethod
    def has_next(self) -> bool:
        pass

    @abc.abstractmethod
    def get_next_api_responses(self) -> List[resp.APIResp]:
        pass

    @abc.abstractmethod
    def _get_next_date_url_param(self) -> Dict[str, Any]:
        pass
