######################################################
#
# Author: Davide Colombo
# Date: 18/11/21 14:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.database.util.record.base as base


class LocationRecord(base.RecordBuilder):

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data=sensor_data)
        return sensor_data['geom']['class'](**sensor_data['geom']['kwargs']).geom_from_text()

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        if 'geom' not in sensor_data:
            raise SystemExit(f"{LocationRecord.__name__} bad sensor data => missing key='geom'")
        if not sensor_data['geom']:
            raise SystemExit(f"{LocationRecord.__name__} bad sensor data => 'geom' cannot be empty")
        if 'class' not in sensor_data['geom'] or 'kwargs' not in sensor_data['geom']:
            raise SystemExit(f"{LocationRecord.__name__} bad sensor data => 'geom' must have 'class' and 'kwargs' keys")
