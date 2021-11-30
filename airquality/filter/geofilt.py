######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.filter.basefilt as base
import airquality.types.apiresp.inforesp as resp


class GeoFilter(base.BaseFilter):

    def __init__(self, log_filename="log"):
        super(GeoFilter, self).__init__(log_filename=log_filename)
        self._database_locations = None

    def with_database_locations(self, active_locations: Dict[str, Any]):
        self._database_locations = active_locations

    def filter(self, resp2filter: List[resp.SensorInfoResponse]) -> List[resp.SensorInfoResponse]:

        all_responses = len(resp2filter)

        # Filter out inactive sensors
        count = 0
        item_idx = 0
        while count < all_responses:
            if not resp2filter[item_idx].sensor_name in self._database_locations:
                self.log_warning(f"{GeoFilter.__name__}: skip sensor '{resp2filter[item_idx].sensor_name}' => not in database")
                del resp2filter[item_idx]
            else:
                item_idx += 1
            count += 1

        if not resp2filter:
            self.log_info(f"{GeoFilter.__name__}: found 0/{all_responses} database sensors")
            return resp2filter

        # Filter active locations there are in the same position
        database_sensors = len(resp2filter)
        count = 0
        item_idx = 0
        while count < database_sensors:
            if resp2filter[item_idx].geolocation.geometry.as_text() == \
                   self._database_locations[resp2filter[item_idx].sensor_name]:
                del resp2filter[item_idx]
            else:
                self.log_info(f"{GeoFilter.__name__}: add sensor '{resp2filter[item_idx].sensor_name}' => new location")
                item_idx += 1
            count += 1

        self.log_info(f"{GeoFilter.__name__}: found {database_sensors}/{all_responses} database sensors")
        self.log_info(f"{GeoFilter.__name__}: found {len(resp2filter)}/{database_sensors} new locations")
        return resp2filter
