######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import List
import airquality.logger.util.decorator as log_decorator
import airquality.filter.filter as base
import airquality.types.apiresp.inforesp as resp


class NameFilter(base.FilterABC):

    def __init__(self, log_filename="log"):
        super(NameFilter, self).__init__(log_filename=log_filename)
        self.database_sensor_names = []

    def with_database_sensor_names(self, names: List[str]):
        self.database_sensor_names = names
        return self

    ################################ filter() ###############################
    @log_decorator.log_decorator()
    def filter(self, resp2filter: List[resp.SensorInfoResponse]) -> List[resp.SensorInfoResponse]:

        if not resp2filter:
            self.log_warning(f"{self.__class__.__name__} found empty responses => return")
            return resp2filter

        tot = len(resp2filter)
        resp2filter = self.filter_out_known_sensors(resp2filter)
        self.log_info(f"{self.__class__.__name__}: found {len(resp2filter)}/{tot} new sensors")

        return resp2filter

    ################################ filter_out_known_sensors() ###############################
    @log_decorator.log_decorator()
    def filter_out_known_sensors(self, responses: List[resp.SensorInfoResponse]) -> List[resp.SensorInfoResponse]:
        tot = len(responses)
        count_iter = itertools.count(0)
        item_iter = itertools.count(0)
        item_idx = next(item_iter)
        while next(count_iter) < tot:
            item = responses[item_idx]
            if item.sensor_name in self.database_sensor_names:
                self.log_warning(f"{self.__class__.__name__} skip known sensor {item.sensor_name}")
                del responses[item_idx]
            else:
                self.log_info(f"{self.__class__.__name__} found new sensor {item.sensor_name}")
                item_idx = next(item_iter)
        return responses
