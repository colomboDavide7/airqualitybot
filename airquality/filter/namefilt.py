######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import List
import airquality.filter.basefilt as base
import airquality.types.apiresp.inforesp as resp
import airquality.database.repo.info_repo as dbrepo


class NameFilter(base.BaseFilter):

    def __init__(self, repo: dbrepo.SensorInfoRepository, log_filename="log"):
        super(NameFilter, self).__init__(log_filename=log_filename)
        self._repo = repo

    def filter(self, resp2filter: List[resp.SensorInfoResponse]) -> List[resp.SensorInfoResponse]:
        database_sensor_names = self.get_database_sensor_names()

        all_responses = len(resp2filter)
        response_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(response_iter) < all_responses:
            if resp2filter[item_idx].sensor_name in database_sensor_names:
                self.log_warning(f"{NameFilter.__name__}: skip sensor '{resp2filter[item_idx].sensor_name}' => already present")
                del resp2filter[item_idx]
            else:
                self.log_info(f"{NameFilter.__name__}: add sensor '{resp2filter[item_idx].sensor_name}' => new sensor")
                item_idx = next(item_iter)

        self.log_info(f"{NameFilter.__name__}: found {len(resp2filter)}/{all_responses} new sensors")
        return resp2filter

    def get_database_sensor_names(self):
        return [r.sensor_name for r in self._repo.lookup()]
