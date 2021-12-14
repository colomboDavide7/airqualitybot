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

RESPONSE_TYPE = List[resptype.InfoAPIRespTypeABC]


# ------------------------------- GeolocationFilter ------------------------------- #
class GeolocationFilter(filterabc.FilterABC):

    def __init__(self, name2geom_as_text: Dict[str, str]):
        super(GeolocationFilter, self).__init__()
        self._name2geom_as_text = name2geom_as_text

    ################################ filter() ################################
    def filter(self, all_resp: RESPONSE_TYPE) -> RESPONSE_TYPE:
        tot = len(all_resp)
        known_locations_responses = self.purge_responses_from_unknown_locations(all_resp)
        self.log_info(f"{self.__class__.__name__} found {len(known_locations_responses)}/{tot} active location")

        tot = len(known_locations_responses)
        changed_known_locations_responses = self.purge_responses_from_unchanged_known_locations(known_locations_responses)
        self.log_info(f"{self.__class__.__name__} found {len(changed_known_locations_responses)}/{tot} new locations")

        return changed_known_locations_responses

    ################################ purge_responses_from_unknown_locations() ################################
    def purge_responses_from_unknown_locations(self, responses: RESPONSE_TYPE) -> RESPONSE_TYPE:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            name = responses[item_idx].sensor_name()
            if name not in self._name2geom_as_text:
                self.log_warning(f"{self.__class__.__name__} skip unknown sensor '{name}'")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__} found known sensor '{name}'")
                item_idx = next(item_iter)
        return responses

    ################################ purge_responses_from_unchanged_known_locations() ################################
    def purge_responses_from_unchanged_known_locations(self, responses: RESPONSE_TYPE) -> RESPONSE_TYPE:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            item = responses[item_idx]
            name = item.sensor_name()
            geom = item.geolocation().as_text()
            if geom == self._name2geom_as_text[name]:
                self.log_warning(f"{self.__class__.__name__} skip sensor '{name}'")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__} found new location for sensor '{name}'")
                item_idx = next(item_iter)
        return responses
