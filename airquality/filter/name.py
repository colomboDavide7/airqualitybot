######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.filter.base as base


class NameFilter(base.BaseFilter):

    def __init__(self, database_sensor_names: List[str]):
        super(NameFilter, self).__init__()
        self.database_sensor_names = database_sensor_names

    def filter(self, to_filter: List[base.baseadpt.BaseUniformModel]) -> List[base.baseadpt.BaseUniformModel]:
        filtered_data = []
        for data in to_filter:
            pass

            # if container.identity.name in self.database_sensor_names:
            #     filtered_containers.append(container)
            #     self.log_info(f"{NameFilter.__name__}: add sensor '{container.identity.name}' => new sensor")
            # else:
            #     self.log_warning(f"{NameFilter.__name__}: skip sensor '{container.identity.name}' => already present")

        # self.log_info(f"{NameFilter.__name__}: found {len(filtered_containers)}/{len(containers)} new sensors")
        return filtered_data
