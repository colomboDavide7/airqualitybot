######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 11:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.database.util.record.base as base
import airquality.adapter.config as c


class TimeRecord(base.RecordBuilder):

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        return f"'{sensor_data[c.TIMEST][c.CLS](**sensor_data[c.TIMEST][c.KW]).get_formatted_timestamp()}'"

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        msg = f"{TimeRecord.__name__}: bad sensor data =>"

        if c.TIMEST not in sensor_data:
            raise SystemExit(f"{msg} missing key='{c.TIMEST}'")
        if not sensor_data[c.TIMEST]:
            raise SystemExit(f"{msg} '{c.TIMEST}' cannot be empty")
        if c.CLS not in sensor_data[c.TIMEST] or c.KW not in sensor_data[c.TIMEST]:
            raise SystemExit(f"{msg} '{c.TIMEST}' must have '{c.CLS}' and '{c.KW}' keys")
