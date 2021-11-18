######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 11:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.database.util.record.base as base


class TimeRecord(base.RecordBuilder):

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        return f"'{sensor_data['timestamp']['class'](**sensor_data['timestamp']['kwargs']).get_formatted_timestamp()}'"

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        if 'timestamp' not in sensor_data:
            raise SystemExit(f"{TimeRecord.__name__}: bad sensor data => missing key='geom'")
        if not sensor_data['timestamp']:
            raise SystemExit(f"{TimeRecord.__name__}: bad sensor data => 'geom' cannot be empty")
        if 'class' not in sensor_data['timestamp'] or 'kwargs' not in sensor_data['timestamp']:
            raise SystemExit(f"{TimeRecord.__name__}: bad sensor data => 'geom' must have 'class' and 'kwargs' keys")
