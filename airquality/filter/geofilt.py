######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.filter.basefilt as base


class GeoFilter(base.BaseFilter):

    def __init__(self, database_active_locations: Dict[str, Any]):
        super(GeoFilter, self).__init__(log_filename=log_filename)
        self.database_active_locations = database_active_locations

    def filter(self, containers: List[sensor_c.SensorContainer]) -> List[sensor_c.SensorContainer]:
        filtered_containers = []
        for container in containers:
            if container.identity.name in self.database_active_locations:
                if container.location.postgis_geom.as_text() != self.database_active_locations[container.identity.name]:
                    filtered_containers.append(container)
                    self.log_info(f"{GeoFilter.__name__}: add sensor '{container.identity.name}' => new location")
                else:
                    self.log_warning(f"{GeoFilter.__name__}: skip sensor '{container.identity.name}' => same location")
            else:
                self.log_warning(f"{GeoFilter.__name__}: skip sensor '{container.identity.name}' => inactive")

        self.log_info(f"{GeoFilter.__name__}: found {len(filtered_containers)}/{len(containers)} new locations")
        return filtered_containers
