######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import Dict, List
import airquality.filter.abc as filterabc
import airquality.api.resp.abc as resptype


# ------------------------------- GeolocationFilter ------------------------------- #
class GeolocationFilter(filterabc.FilterABC):

    def __init__(self, name2geom_as_text: Dict[str, str]):
        super(GeolocationFilter, self).__init__()
        self._name2geom_as_text = name2geom_as_text

    ################################ filter() ################################
    def filter(self, all_resp: List[resptype.InfoAPIRespTypeABC]) -> List[resptype.InfoAPIRespTypeABC]:
        tot = len(all_resp)
        active_locations = self.delete_unknown_locations(all_resp)
        self.log_info(f"{self.__class__.__name__} found {len(active_locations)}/{tot} active location")

        tot = len(active_locations)
        new_locations = self.delete_unchanged_locations(active_locations)
        self.log_info(f"{self.__class__.__name__} found {len(new_locations)}/{tot} new locations")

        return new_locations

    ################################ delete_unknown_locations() ################################
    def delete_unknown_locations(self, responses: List[resptype.InfoAPIRespTypeABC]) -> List[resptype.InfoAPIRespTypeABC]:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            item = responses[item_idx]
            name = item.sensor_name()
            if name not in self._name2geom_as_text:
                self.log_warning(f"{self.__class__.__name__}: skip unknown location {name}")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__}: found known location {name}")
                item_idx = next(item_iter)
        return responses

    ################################ delete_unchanged_locations() ################################
    def delete_unchanged_locations(self, responses: List[resptype.InfoAPIRespTypeABC]) -> List[resptype.InfoAPIRespTypeABC]:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            item = responses[item_idx]
            name = item.sensor_name()
            if item.geolocation().as_text() == self._name2geom_as_text[name]:
                self.log_warning(f"{self.__class__.__name__}: skip sensor {name}")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__}: found new location for {name}")
                item_idx = next(item_iter)
        return responses
