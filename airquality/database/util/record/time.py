######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 11:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.database.util.record.base as base
import airquality.database.util.datatype.timestamp as ts


class TimeRecord(base.RecordBuilder):

    def __init__(self, timestamp_class=ts.SQLTimestamp):
        self.timestamp_class = timestamp_class

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        return f"'{self.timestamp_class(sensor_data['timestamp']).ts}'"

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        if sensor_data.get('timestamp') is None:
            raise SystemExit(f"{TimeRecord.__name__}: bad sensor data => missing required key='timestamp'")


################################ CURRENT TIMESTAMP TIME RECORD ################################
class CurrentTimestampTimeRecord(base.RecordBuilder):

    def __init__(self, timestamp_class=ts.CurrentTimestamp):
        self.timestamp_class = timestamp_class

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data=sensor_data)
        return f"'{self.timestamp_class().ts}'"

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        pass
