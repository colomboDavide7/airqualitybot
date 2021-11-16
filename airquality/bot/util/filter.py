######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.database.util.datatype.timestamp as ts
import airquality.logger.loggable as log


def get_packet_filter(bot_name: str):

    if bot_name == 'fetch':
        return TimestampFilter()
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
                self.info_messages.append(f"found new sensor '{data['name']}'")
            else:
                self.warning_messages.append(f"skip sensor '{data['name']}' => already present")

        # Log messages
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
                self.info_messages.append(f"found active location '{data['name']}'")
            else:
                self.warning_messages.append(f"skip location '{data['name']}' => not active")

        self.log_messages()

        return filtered_packets


################################ DATE FILTER ################################
class TimestampFilter(SensorDataFilter):

    def __init__(self):
        super(TimestampFilter, self).__init__()
        self.filter_ts = None

    def set_filter_ts(self, filter_ts=ts.SQLTimestamp):
        self.filter_ts = filter_ts

    def filter(self, sensor_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        # Raise SystemExit if 'filter_ts' external dependency is missing
        if not self.filter_ts:
            raise SystemExit(f"{TimestampFilter.__name__}: bad setup => missing external dependency 'filter_ts'")

        # Filter the measurements: keep only those packets that came after the 'filter_ts'
        fetched_new_measures = []
        for packet in sensor_data:
            timestamp = packet['timestamp']
            if timestamp.is_after(self.filter_ts):
                fetched_new_measures.append(packet)

        # Debug and log new measurement timestamp range
        if fetched_new_measures:
            first_timestamp = fetched_new_measures[0]['timestamp']
            last_timestamp = fetched_new_measures[-1]['timestamp']
            self.info_messages.append(f"found new measurements from {first_timestamp.ts} to {last_timestamp.ts}")

        # Log messages
        self.log_messages()

        return fetched_new_measures
