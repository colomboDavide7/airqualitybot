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

RESPONSE_TYPE = List[resptype.InfoAPIRespTypeABC]


# ------------------------------- NameFilter ------------------------------- #
class NameFilter(filterabc.FilterABC):

    def __init__(self, names: List[str]):
        super().__init__()
        self._known_names = names

    ################################ filter() ###############################
    def filter(self, all_resp: RESPONSE_TYPE) -> RESPONSE_TYPE:
        tot = len(all_resp)
        all_resp = self.purge_responses_from_known_sensors(all_resp)
        self.log_info(f"{self.__class__.__name__}: found {len(all_resp)}/{tot} new sensors")
        return all_resp

    ################################ purge_responses_from_known_sensors() ###############################
    def purge_responses_from_known_sensors(self, responses: RESPONSE_TYPE) -> RESPONSE_TYPE:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            name = responses[item_idx].sensor_name()
            if name in self._known_names:
                self.log_warning(f"{self.__class__.__name__} skip known sensor {name}")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__} found new sensor {name}")
                item_idx = next(item_iter)
        return responses
