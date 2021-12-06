######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import itertools
import airquality.filter.basefilt as base
import airquality.types.apiresp.inforesp as resp
import airquality.database.repo.geo_repo as dbrepo


class GeoFilter(base.BaseFilter):

    def __init__(self, repo: dbrepo.SensorGeoRepository, log_filename="log"):
        super(GeoFilter, self).__init__(log_filename=log_filename)
        self._repo = repo

    ################################ filter() ################################
    def filter(self, resp2filter: List[resp.SensorInfoResponse]) -> List[resp.SensorInfoResponse]:

        all_responses = len(resp2filter)
        database_locations = self.get_database_location()

        # Filter out inactive sensors
        resp2filter = self.filter_inactive_locations(responses=resp2filter, database_locations=database_locations)
        if not resp2filter:
            self.log_info(f"{GeoFilter.__name__}: found 0/{all_responses} database sensors")
            return resp2filter

        # Filter active locations there are in the same position
        database_sensors = len(resp2filter)
        resp2filter = self.filter_same_locations(responses=resp2filter, database_locations=database_locations)

        self.log_info(f"{GeoFilter.__name__}: found {database_sensors}/{all_responses} database sensors")
        self.log_info(f"{GeoFilter.__name__}: found {len(resp2filter)}/{database_sensors} new locations")
        return resp2filter

    ################################ filter_same_locations() ################################
    def filter_same_locations(
            self, responses: List[resp.SensorInfoResponse], database_locations: Dict[str, Any]
    ) -> List[resp.SensorInfoResponse]:

        all_responses = len(responses)
        response_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(response_iter) < all_responses:
            if responses[item_idx].geolocation.geometry.as_text() == database_locations[responses[item_idx].sensor_name]:
                self.log_warning(f"{GeoFilter.__name__}: skip sensor '{responses[item_idx].sensor_name}' => same location")
                del responses[item_idx]
            else:
                self.log_info(f"{GeoFilter.__name__}: add sensor '{responses[item_idx].sensor_name}' => new location")
                item_idx = next(item_iter)
        return responses

    ################################ filter_inactive_locations() ################################
    def filter_inactive_locations(
            self, responses: List[resp.SensorInfoResponse], database_locations: Dict[str, Any]
    ) -> List[resp.SensorInfoResponse]:

        all_responses = len(responses)
        response_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(response_iter) < all_responses:
            if responses[item_idx].sensor_name not in database_locations:
                self.log_warning(f"{GeoFilter.__name__}: skip sensor '{responses[item_idx].sensor_name}' => not in database")
                del responses[item_idx]
            else:
                item_idx = next(item_iter)
        return responses

    ################################ get_database_locations() ################################
    def get_database_location(self) -> Dict[str, Any]:
        return {single_lookup.sensor_name: single_lookup.geometry.as_text() for single_lookup in self._repo.lookup()}
