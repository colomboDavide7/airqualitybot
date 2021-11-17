######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.logger.loggable as log
import airquality.database.util.postgis.geom as geom
import airquality.database.util.datatype.timestamp as ts
import airquality.database.operation.select as select


################################ SENSOR DATA FILTER BASE CLASS ################################
class SensorDataFilter(log.Loggable):

    @abc.abstractmethod
    def filter(self, sensor_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def _log_message(self, n_total: int, n_filtered: int):
        pass


################################ NAME FILTER ################################
class NameFilter(SensorDataFilter):

    def __init__(self, database_sensor_names: List[str]):
        super(NameFilter, self).__init__()
        self.database_sensor_names = database_sensor_names

    def filter(self, sensor_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        filtered_data = [data for data in sensor_data if data['name'] not in self.database_sensor_names]

        self._log_message(n_total=len(sensor_data), n_filtered=len(filtered_data))
        return filtered_data

    def _log_message(self, n_total: int, n_filtered: int):
        msg = f"{NameFilter.__name__} found {n_filtered}/{n_total} new sensors"
        if n_filtered == 0:
            self.warning_messages.append(msg)
        else:
            self.info_messages.append(msg)
        self.log_messages()


################################ TIMESTAMP FILTER ################################
class TimestampFilter(SensorDataFilter):

    def __init__(self, timestamp_class):
        super(TimestampFilter, self).__init__()
        self.timestamp_class = timestamp_class
        self.filter_ts = None

    def set_filter_ts(self, filter_ts=ts.SQLTimestamp):
        self.filter_ts = filter_ts

    def filter(self, sensor_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        # Raise SystemExit if 'filter_ts' external dependency is missing
        if not self.filter_ts:
            raise SystemExit(f"{TimestampFilter.__name__}: bad setup => missing external dependency 'filter_ts'")

        filtered_data = [data for data in sensor_data if self.timestamp_class(data['timestamp']).is_after(self.filter_ts)]
        self._log_message(n_total=len(sensor_data), n_filtered=len(filtered_data))
        return filtered_data

    def _log_message(self, n_total: int, n_filtered: int):
        msg = f"{TimestampFilter.__name__} found {n_filtered}/{n_total} new measurements"
        if n_filtered == 0:
            self.warning_messages.append(msg)
        else:
            self.info_messages.append(msg)
        self.log_messages()


################################ GEO FILTER ################################
class GeoFilter(SensorDataFilter):

    def __init__(self, postgis_builder: geom.GeometryBuilder, database_active_locations: Dict[str, Any]):
        super(GeoFilter, self).__init__()
        self.postgis_builder = postgis_builder
        self.database_active_locations = database_active_locations

    def filter(self, sensor_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        active_sensors = [data for data in sensor_data if data['name'] in self.database_active_locations]
        if not active_sensors:
            self.warning_messages.append(f"{GeoFilter.__name__} has not found active sensors")
            self.log_messages()
            return []

        changed_sensors = [data for data in active_sensors
                           if self.postgis_builder.as_text(data) != self.database_active_locations[data['name']]]

        self._log_message(n_total=len(sensor_data), n_filtered=len(changed_sensors))
        return changed_sensors

    def _log_message(self, n_total: int, n_filtered: int):
        msg = f"{GeoFilter.__name__} found {n_filtered}/{n_total} new locations"
        if n_filtered == 0:
            self.warning_messages.append(msg)
        else:
            self.info_messages.append(msg)
        self.log_messages()


################################ GET FUNCTION ################################
def get_sensor_data_filter(bot_name: str, sensor_type: str, sel_wrapper: select.SensorTypeSelectWrapper) -> SensorDataFilter:

    if bot_name == 'init':
        database_sensor_names = sel_wrapper.get_sensor_names()
        return NameFilter(database_sensor_names=database_sensor_names)
    elif bot_name == 'update':
        active_locations = sel_wrapper.get_active_locations()
        return GeoFilter(postgis_builder=geom.PointBuilder(), database_active_locations=active_locations)
    elif bot_name == 'fetch':
        timestamp_class = ts.get_timestamp_class(sensor_type=sensor_type)
        return TimestampFilter(timestamp_class=timestamp_class)
    else:
        raise SystemExit(f"'{get_sensor_data_filter.__name__}():' bad name '{bot_name}'")
