######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, Generator
import airquality.filter.filter as base
import airquality.types.apiresp.inforesp as resp


class GeoFilter(base.FilterABC):

    def __init__(self, log_filename="log"):
        super(GeoFilter, self).__init__(log_filename=log_filename)
        self._database_locations = {}

    def with_database_locations(self, locations: Dict[str, Any]):
        self._database_locations = locations
        return self

    ################################ filter() ################################
    def filter(self, resp2filter: Generator[resp.SensorInfoResponse, None, None]) -> Generator[resp.SensorInfoResponse, None, None]:

        active_locations = self.filter_inactive_locations(resp2filter)
        new_locations = self.filter_same_locations(active_locations)
        return new_locations

    ################################ filter_inactive_locations() ################################
    def filter_inactive_locations(
            self, responses: Generator[resp.SensorInfoResponse, None, None]
    ) -> Generator[resp.SensorInfoResponse, None, None]:
        for response in responses:
            if response.sensor_name in self._database_locations:
                self.log_info(f"{self.__class__.__name__}: found active location '{response.sensor_name}'")
                yield response

    ################################ filter_same_locations() ################################
    def filter_same_locations(
            self, responses: Generator[resp.SensorInfoResponse, None, None]
    ) -> Generator[resp.SensorInfoResponse, None, None]:
        for response in responses:
            if response.geolocation.geometry.as_text() != self._database_locations[response.sensor_name]:
                self.log_info(f"{self.__class__.__name__}: found new location for '{response.sensor_name}'")
                yield response
