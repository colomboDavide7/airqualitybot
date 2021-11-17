######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.database.util.postgis.geom as geom
import airquality.database.util.datatype.timestamp as ts
import airquality.logger.loggable as log


def get_sensor_data_filter(bot_name: str, sensor_type: str):

    if bot_name == 'fetch':
        if sensor_type == 'atmotube':
            return TimestampFilter(timestamp_class=ts.AtmotubeTimestamp)
        elif sensor_type == 'thingspeak':
            return TimestampFilter(timestamp_class=ts.ThingspeakTimestamp)
        else:
            raise SystemExit(f"{get_sensor_data_filter.__name__}(): bad type '{sensor_type}' for bot '{bot_name}'")
    elif bot_name == 'init':
        return NameFilter()
    elif bot_name == 'update':
        return NameKeeper()


################################ PACKET FILTER BASE CLASS ################################
class SensorDataFilter(log.Loggable):

    @abc.abstractmethod
    def filter(self, sensor_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass


################################ NAME FILTER ################################
class NameFilter(SensorDataFilter):

    def __init__(self):
        super(NameFilter, self).__init__()
        self.name_to_filter = None

    def set_name_to_filter(self, name_to_filter: List[str]):
        self.name_to_filter = name_to_filter

    def filter(self, sensor_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        # Check if external dependency was set
        if self.name_to_filter is None:
            raise SystemExit(f"{NameFilter.__name__}: bad setup => missing external dependency 'database_sensor_names'")

        # Filter packets: keep only those packets which name is inside the 'database_sensor_names'
        filtered_packets = []
        for data in sensor_data:
            if data['name'] not in self.name_to_filter:
                filtered_packets.append(data)
                self.info_messages.append(f"{NameFilter.__name__} found new sensor '{data['name']}'")
            else:
                self.warning_messages.append(f"{NameFilter.__name__} skipped existing sensor '{data['name']}'")
        self.log_messages()
        return filtered_packets


class NameKeeper(SensorDataFilter):

    def __init__(self):
        super(NameKeeper, self).__init__()
        self.name_to_keep = None

    def set_name_to_keep(self, name_to_keep: List[str]):
        self.name_to_keep = name_to_keep

    def filter(self, sensor_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        if self.name_to_keep is None:
            raise SystemExit(f"{NameKeeper.__name__}: bad setup => missing external dependency 'name_to_keep'")

        filtered_packets = []
        for data in sensor_data:
            if data['name'] in self.name_to_keep:
                filtered_packets.append(data)
                self.info_messages.append(f"{NameKeeper.__name__} found active location '{data['name']}'")
            else:
                self.warning_messages.append(f"{NameKeeper.__name__} skipped non-active location '{data['name']}'")
        self.log_messages()
        return filtered_packets


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

        # Filter the measurements: keep only those packets that came after the 'filter_ts'
        filtered_data = []
        for packet in sensor_data:
            timestamp = self.timestamp_class(packet['timestamp'])
            if timestamp.is_after(self.filter_ts):
                filtered_data.append(packet)
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

    def __init__(self, postgis_builder: geom.GeometryBuilder):
        super(GeoFilter, self).__init__()
        self.postgis_builder = postgis_builder
        self.database_active_locations = None

    def set_database_active_locations(self, locations: Dict[str, Any]):
        self.database_active_locations = locations

    def filter(self, sensor_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        if self.database_active_locations is None:
            raise SystemExit(f"{GeoFilter.__name__}: bad setup => missing external dependency 'database_active_locations'")

        changed_sensors = []
        for data in sensor_data:
            sensor_name = data['name']
            old_geom = self.database_active_locations[sensor_name]
            new_geom = self.postgis_builder.as_text(sensor_data=data)
            if new_geom != old_geom:
                changed_sensors.append(data)
        return changed_sensors
