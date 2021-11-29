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
        filtered_responses = []
        for response in resp2filter:
            if response.sensor_name not in self._database_sensor_names:
                filtered_responses.append(response)
                self.log_info(f"{NameFilter.__name__}: add sensor '{response.sensor_name}' => new sensor")
            else:
                self.log_warning(f"{NameFilter.__name__}: skip sensor '{response.sensor_name}' => already present")

        self.log_info(f"{NameFilter.__name__}: found {len(filtered_responses)}/{len(resp2filter)} new sensors")
        return filtered_responses
