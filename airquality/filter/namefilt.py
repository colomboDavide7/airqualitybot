######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.filter.basefilt as base
import airquality.types.apiresp.inforesp as resp


class NameFilter(base.BaseFilter):

    def __init__(self, log_filename="log"):
        super(NameFilter, self).__init__(log_filename=log_filename)
        self._database_sensor_names = None

    def with_database_sensor_names(self, dbnames: List[str]):
        self._database_sensor_names = dbnames
        return self

    def filter(self, resp2filter: List[resp.SensorInfoResponse]) -> List[resp.SensorInfoResponse]:
        all_responses = len(resp2filter)
        count = 0
        item_idx = 0
        while count < all_responses:
            if resp2filter[item_idx].sensor_name in self._database_sensor_names:
                self.log_warning(f"{NameFilter.__name__}: skip sensor '{resp2filter[item_idx].sensor_name}' => already present")
                del resp2filter[item_idx]
            else:
                self.log_info(f"{NameFilter.__name__}: add sensor '{resp2filter[item_idx].sensor_name}' => new sensor")
                item_idx += 1
            count += 1

        self.log_info(f"{NameFilter.__name__}: found {len(resp2filter)}/{all_responses} new sensors")
        return resp2filter
