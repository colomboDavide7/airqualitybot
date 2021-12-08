######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Generator
import airquality.filter.filter as base
import airquality.types.apiresp.inforesp as resp


class NameFilter(base.FilterABC):

    def __init__(self, log_filename="log"):
        super(NameFilter, self).__init__(log_filename=log_filename)
        self.database_sensor_names = []

    def with_database_sensor_names(self, names: List[str]):
        self.database_sensor_names = names
        return self

    def filter(self, resp2filter: List[resp.SensorInfoResponse]) -> Generator[resp.SensorInfoResponse, None, None]:
        for response in resp2filter:
            if response.sensor_name not in self.database_sensor_names:
                self.log_info(f"{self.__class__.__name__}: found new sensor '{response.sensor_name}'")
                yield response
