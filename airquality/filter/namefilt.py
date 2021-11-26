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

    def __init__(self, database_sensor_names: List[str], log_filename="log"):
        super(NameFilter, self).__init__(log_filename=log_filename)
        self.database_sensor_names = database_sensor_names

    # ************************************ filter ************************************
    def filter(self, resp2filter: List[resp.SensorInfoResponse]) -> List[resp.SensorInfoResponse]:
        filtered_responses = []
        for response in resp2filter:
            if response.sensor_name not in self.database_sensor_names:
                filtered_responses.append(response)
                self.log_info(f"{NameFilter.__name__}: add sensor '{response.sensor_name}' => new sensor")
            else:
                self.log_warning(f"{NameFilter.__name__}: skip sensor '{response.sensor_name}' => already present")

        self.log_info(f"{NameFilter.__name__}: found {len(filtered_responses)}/{len(resp2filter)} new sensors")
        return filtered_responses
