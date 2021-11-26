######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.filter.basefilt as base
import airquality.types.apiresp.inforesp as resp


class GeoFilter(base.BaseFilter):

    def __init__(self, database_active_locations: Dict[str, Any], log_filename="log"):
        super(GeoFilter, self).__init__(log_filename=log_filename)
        self.database_active_locations = database_active_locations

    # ************************************ filter ************************************
    def filter(self, resp2filter: List[resp.SensorInfoResponse]) -> List[resp.SensorInfoResponse]:
        filtered_responses = []
        for response in resp2filter:
            if response.sensor_name in self.database_active_locations:
                if response.geolocation.geometry.as_text() != self.database_active_locations[response.sensor_name]:
                    filtered_responses.append(response)
                    self.log_info(f"{GeoFilter.__name__}: add sensor '{response.sensor_name}' => new location")
                else:
                    self.log_warning(f"{GeoFilter.__name__}: skip sensor '{response.sensor_name}' => same location")
            else:
                self.log_warning(f"{GeoFilter.__name__}: skip sensor '{response.sensor_name}' => inactive")

        self.log_info(f"{GeoFilter.__name__}: found {len(filtered_responses)}/{len(resp2filter)} new locations")
        return filtered_responses
