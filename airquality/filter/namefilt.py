######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.filter.basefilt as base
import airquality.adapter.api2db.initadapt.initadapt as initadapt


class NameFilter(base.BaseFilter):

    def __init__(self, database_sensor_names: List[str]):
        super(NameFilter, self).__init__()
        self.database_sensor_names = database_sensor_names

    def filter(self, to_filter: List[initadapt.InitUniformModel]) -> List[initadapt.InitUniformModel]:
        filtered_data = []
        for data in to_filter:
            if data.name in self.database_sensor_names:
                filtered_data.append(data)
                self.log_info(f"{NameFilter.__name__}: add sensor '{data.name}' => new sensor")
            else:
                self.log_warning(f"{NameFilter.__name__}: skip sensor '{data.name}' => already present")

        self.log_info(f"{NameFilter.__name__}: found {len(filtered_data)}/{len(to_filter)} new sensors")
        return filtered_data
