######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 14/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.database.util.datatype.timestamp as ts
import airquality.logger.log as log


################################ PACKET FILTER BASE CLASS ################################
class PacketFilter(abc.ABC):

    def __init__(self):
        self.logger = None
        self.debugger = None

    def set_logger(self, logger: log.logging.Logger):
        self.logger = logger

    def set_debugger(self, debugger: log.logging.Logger):
        self.debugger = debugger

    @abc.abstractmethod
    def filter(self,  packets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass


################################ NAME FILTER ################################
class NameFilter(PacketFilter):

    def __init__(self):
        super(NameFilter, self).__init__()
        self.database_sensor_names = None

    def set_database_sensor_names(self, database_sensor_names: List[str]):
        self.database_sensor_names = database_sensor_names

    def filter(self,  packets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        # Check if external dependency was set
        if self.database_sensor_names is None:
            raise SystemExit(f"{NameFilter.__name__}: bad setup => missing external dependency 'database_sensor_names'")

        # Filter packets: keep only those packets which name is inside the 'database_sensor_names'
        logging_msg = []
        fetched_new_sensors = []
        for uniformed_packet in packets:
            if uniformed_packet['name'] not in self.database_sensor_names:
                fetched_new_sensors.append(uniformed_packet)
                logging_msg.append(f"found new sensor '{uniformed_packet['name']}'")
            else:
                logging_msg.append(f"skip sensor '{uniformed_packet['name']}' => already present")

        # Log messages
        if self.logger:
            for msg in logging_msg:
                if msg.startswith('skip'):
                    self.logger.warning(msg)
                else:
                    self.logger.info(msg)

        # Debug messages
        if self.debugger:
            for msg in logging_msg:
                if msg.startswith('skip'):
                    self.debugger.warning(msg)
                else:
                    self.debugger.info(msg)

        return fetched_new_sensors


################################ DATE FILTER ################################
class DateFilter(PacketFilter):

    def __init__(self, timest_cls=ts.SQLTimestamp):
        super(DateFilter, self).__init__()
        self.timest_cls = timest_cls
        self.filter_ts = None

    def set_filter_ts(self, filter_ts=ts.SQLTimestamp):
        self.filter_ts = filter_ts

    def filter(self, packets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        # Raise SystemExit if 'filter_ts' external dependency is missing
        if not self.filter_ts:
            raise SystemExit(f"{DateFilter.__name__}: bad setup => missing external dependency 'filter_ts'")

        # Filter the measurements: keep only those packets that came after the 'filter_ts'
        fetched_new_measures = []
        for packet in packets:
            timestamp = self.timest_cls(packet['timestamp'])
            if timestamp.is_after(self.filter_ts):
                fetched_new_measures.append(packet)

        # Debug and log new measurement timestamp range
        if fetched_new_measures:
            first_timestamp = fetched_new_measures[0]['timestamp']
            last_timestamp = fetched_new_measures[-1]['timestamp']
            if self.debugger:
                self.debugger.info(f"found new measurements from {first_timestamp} to {last_timestamp}")
            if self.logger:
                self.logger.info(f"found new measurements from {first_timestamp} to {last_timestamp}")

        return fetched_new_measures
