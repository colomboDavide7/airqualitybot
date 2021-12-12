######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import Dict, Any, List
import airquality.filter.abc as filterabc
import airquality.api.resp.abc as resptype


class GeoFilter(filterabc.FilterABC):

    def __init__(self, locations: Dict[str, Any]):
        super(GeoFilter, self).__init__()
        self._database_locations = locations

    ################################ filter() ################################
    def filter(self, all_resp: List[resptype.InfoAPIRespTypeABC]) -> List[resptype.InfoAPIRespTypeABC]:
        if not all_resp:
            self.log_warning(f"{self.__class__.__name__} found empty responses => return")
            return all_resp

        tot = len(all_resp)
        active_locations = self.filter_inactive_locations(all_resp)
        self.log_info(f"{self.__class__.__name__} found {len(active_locations)}/{tot} active location")

        tot = len(active_locations)
        new_locations = self.filter_same_locations(active_locations)
        self.log_info(f"{self.__class__.__name__} found {len(new_locations)}/{tot} new locations")

        return new_locations

    ################################ filter_inactive_locations() ################################
    def filter_inactive_locations(self, responses: List[resptype.InfoAPIRespTypeABC]) -> List[resptype.InfoAPIRespTypeABC]:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            item = responses[item_idx]
            if item.sensor_name() not in self._database_locations:
                self.log_warning(f"{self.__class__.__name__}: skip unknown sensor {item.sensor_name()}")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__}: found known sensor {item.sensor_name()}")
                item_idx = next(item_iter)
        return responses

    ################################ filter_same_locations() ################################
    def filter_same_locations(self, responses: List[resptype.InfoAPIRespTypeABC]) -> List[resptype.InfoAPIRespTypeABC]:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            item = responses[item_idx]
            name = item.sensor_name()
            if item.geolocation().as_text() == self._database_locations[name]:
                self.log_warning(f"{self.__class__.__name__}: skip sensor {name}")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__}: found new location for {name}")
                item_idx = next(item_iter)
        return responses
