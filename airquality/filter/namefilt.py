######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import List
import airquality.logger.util.decorator as log_decorator
import airquality.filter.abc as filterabc
import airquality.api.resp.abc as resptype


class NameFilter(filterabc.FilterABC):

    def __init__(self, names: List[str], log_filename="log"):
        super(NameFilter, self).__init__(log_filename=log_filename)
        self.database_sensor_names = names

    ################################ filter() ###############################
    @log_decorator.log_decorator()
    def filter(self, all_resp: List[resptype.InfoAPIRespType]) -> List[resptype.InfoAPIRespType]:

        if not all_resp:
            self.log_warning(f"{self.__class__.__name__} found empty responses => return")
            return all_resp

        tot = len(all_resp)
        all_resp = self.filter_out_known_sensors(all_resp)
        self.log_info(f"{self.__class__.__name__}: found {len(all_resp)}/{tot} new sensors")

        return all_resp

    ################################ filter_out_known_sensors() ###############################
    @log_decorator.log_decorator()
    def filter_out_known_sensors(self, responses: List[resptype.InfoAPIRespType]) -> List[resptype.InfoAPIRespType]:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            name = responses[item_idx].sensor_name()
            if name in self.database_sensor_names:
                self.log_warning(f"{self.__class__.__name__} skip known sensor {name}")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__} found new sensor {name}")
                item_idx = next(item_iter)
        return responses
