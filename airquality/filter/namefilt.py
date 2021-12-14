######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import List
import airquality.filter.abc as filterabc
import airquality.api.resp.abc as resptype


# ------------------------------- NameFilter ------------------------------- #
class NameFilter(filterabc.FilterABC):

    def __init__(self, names: List[str]):
        super().__init__()
        self._names = names

    ################################ filter() ###############################
    def filter(self, all_resp: List[resptype.InfoAPIRespTypeABC]) -> List[resptype.InfoAPIRespTypeABC]:
        tot = len(all_resp)
        all_resp = self.delete_known_names(all_resp)
        self.log_info(f"{self.__class__.__name__}: found {len(all_resp)}/{tot} new sensors")
        return all_resp

    ################################ delete_known_names() ###############################
    def delete_known_names(self, responses: List[resptype.InfoAPIRespTypeABC]) -> List[resptype.InfoAPIRespTypeABC]:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            name = responses[item_idx].sensor_name()
            if name in self._names:
                self.log_warning(f"{self.__class__.__name__} skip known sensor {name}")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__} found new sensor {name}")
                item_idx = next(item_iter)
        return responses
