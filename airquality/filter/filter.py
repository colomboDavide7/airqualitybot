######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any, Union
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator
import airquality.database.util.datatype.timestamp as ts
import container.sensor.sensor as sensor_c
import container.measure.measure as meas_c


################################ SENSOR DATA FILTER BASE CLASS ################################
class SensorDataFilter(log.Loggable):

    def __init__(self, log_filename="log"):
        super(SensorDataFilter, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def filter(self, containers: List[Union[sensor_c.SensorContainer, meas_c.MeasureContainer]]) -> List[Union[sensor_c.SensorContainer, meas_c.MeasureContainer]]:
        pass


################################ NAME FILTER ################################
class NameFilter(SensorDataFilter):

    def __init__(self, database_sensor_names: List[str], log_filename="log"):
        super(NameFilter, self).__init__(log_filename=log_filename)
        self.database_sensor_names = database_sensor_names

    @log_decorator.log_decorator()
    def filter(self, containers: List[sensor_c.SensorContainer]) -> List[sensor_c.SensorContainer]:
        filtered_containers = []
        for container in containers:
            if container.identity.name in self.database_sensor_names:
                filtered_containers.append(container)
                self.log_info(f"{NameFilter.__name__}: add sensor '{container.identity.name}' => new sensor")
            else:
                self.log_warning(f"{NameFilter.__name__}: skip sensor '{container.identity.name}' => already present")

        self.log_info(f"{NameFilter.__name__}: found {len(filtered_containers)}/{len(containers)} new sensors")
        return filtered_containers


################################ TIMESTAMP FILTER ################################
class TimestampFilter(SensorDataFilter):

    def __init__(self, log_filename="log"):
        super(TimestampFilter, self).__init__(log_filename=log_filename)
        self.filter_ts = None

    def set_filter_ts(self, filter_ts=ts.SQLTimestamp):
        self.filter_ts = filter_ts

    def filter(self, containers: List[meas_c.MeasureContainer]) -> List[meas_c.MeasureContainer]:
        filtered_containers = []
        for container in containers:
            if container.timestamp.is_after(self.filter_ts):
                filtered_containers.append(container)

        self.log_info(f"{TimestampFilter.__name__}: found {len(filtered_containers)}/{len(containers)} new measurements")
        return filtered_containers


################################ GEO FILTER ################################
class GeoFilter(SensorDataFilter):

    def __init__(self, database_active_locations: Dict[str, Any], log_filename="log"):
        super(GeoFilter, self).__init__(log_filename=log_filename)
        self.database_active_locations = database_active_locations

    @log_decorator.log_decorator()
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
