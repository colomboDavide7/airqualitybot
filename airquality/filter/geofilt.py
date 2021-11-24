######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.filter.basefilt as base
import airquality.api2db.updtunif.updtunif as unif


class GeoFilter(base.BaseFilter):

    def __init__(self, database_active_locations: Dict[str, Any], log_filename="log"):
        super(GeoFilter, self).__init__(log_filename=log_filename)
        self.database_active_locations = database_active_locations

    def filter(self, to_filter: List[unif.UpdateUniformResponse]) -> List[unif.UpdateUniformResponse]:
        filtered_data = []
        for data in to_filter:
            if data.sensor_name in self.database_active_locations:
                if data.geolocation.geolocation.as_text() != self.database_active_locations[data.sensor_name]:
                    filtered_data.append(data)
                    self.log_info(f"{GeoFilter.__name__}: add sensor '{data.sensor_name}' => new location")
                else:
                    self.log_warning(f"{GeoFilter.__name__}: skip sensor '{data.sensor_name}' => same location")
            else:
                self.log_warning(f"{GeoFilter.__name__}: skip sensor '{data.sensor_name}' => inactive")

        self.log_info(f"{GeoFilter.__name__}: found {len(filtered_data)}/{len(to_filter)} new locations")
        return filtered_data
