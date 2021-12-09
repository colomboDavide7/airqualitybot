######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import Dict, Any, List
import airquality.filter.filter as base
import airquality.types.apiresp.inforesp as resptype


class GeoFilter(base.FilterABC):

    def __init__(self, log_filename="log"):
        super(GeoFilter, self).__init__(log_filename=log_filename)
        self._database_locations = {}

    def with_database_locations(self, locations: Dict[str, Any]):
        self._database_locations = locations
        return self

    ################################ filter() ################################
    def filter(self, resp2filter: List[resptype.SensorInfoResponse]) -> List[resptype.SensorInfoResponse]:
        if not resp2filter:
            self.log_warning(f"{self.__class__.__name__} found empty responses => return")
            return resp2filter

        tot = len(resp2filter)
        active_locations = self.filter_inactive_locations(resp2filter)
        self.log_info(f"{self.__class__.__name__} found {len(active_locations)}/{tot} active location")

        tot = len(active_locations)
        new_locations = self.filter_same_locations(active_locations)
        self.log_info(f"{self.__class__.__name__} found {len(new_locations)}/{tot} new locations")

        return new_locations

    ################################ filter_inactive_locations() ################################
    def filter_inactive_locations(self, responses: List[resptype.SensorInfoResponse]) -> List[resptype.SensorInfoResponse]:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            item = responses[item_idx]
            if item.sensor_name not in self._database_locations:
                self.log_warning(f"{self.__class__.__name__}: skip unknown sensor {item.sensor_name}")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__}: found known sensor {item.sensor_name}")
                item_idx = next(item_iter)
        return responses

    ################################ filter_same_locations() ################################
    def filter_same_locations(self, responses: List[resptype.SensorInfoResponse]) -> List[resptype.SensorInfoResponse]:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            item = responses[item_idx]
            if item.geolocation.geometry.as_text() == self._database_locations[item.sensor_name]:
                self.log_warning(f"{self.__class__.__name__}: skip sensor {item.sensor_name}")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__}: found new location for {item.sensor_name}")
                item_idx = next(item_iter)
        return responses
