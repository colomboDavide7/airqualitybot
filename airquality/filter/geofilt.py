######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.filter.basefilt as base
import airquality.adapter.api2db.initadapt.initadapt as initadapt


class GeoFilter(base.BaseFilter):

    def __init__(self, database_active_locations: Dict[str, Any]):
        super(GeoFilter, self).__init__()
        self.database_active_locations = database_active_locations

    def filter(self, to_filter: List[initadapt.InitUniformModel]) -> List[initadapt.InitUniformModel]:
        filtered_data = []
        for data in to_filter:
            if data.name in self.database_active_locations:
                if data.geolocation.geolocation.as_text() != self.database_active_locations[data.name]:
                    filtered_data.append(data)
                    self.log_info(f"{GeoFilter.__name__}: add sensor '{data.name}' => new location")
                else:
                    self.log_warning(f"{GeoFilter.__name__}: skip sensor '{data.name}' => same location")
            else:
                self.log_warning(f"{GeoFilter.__name__}: skip sensor '{data.name}' => inactive")

        self.log_info(f"{GeoFilter.__name__}: found {len(filtered_data)}/{len(to_filter)} new locations")
        return filtered_data
