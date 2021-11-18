######################################################
#
# Author: Davide Colombo
# Date: 18/11/21 14:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.database.util.record.base as base
import airquality.adapter.config as c


class LocationRecord(base.RecordBuilder):

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data=sensor_data)
        return sensor_data[c.SENS_GEOM][c.CLS](**sensor_data[c.SENS_GEOM][c.KW]).geom_from_text()

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        msg = f"{LocationRecord.__name__} bad sensor data =>"

        if c.SENS_GEOM not in sensor_data:
            raise SystemExit(f"{msg} missing key='{c.SENS_GEOM}'")
        if not sensor_data[c.SENS_GEOM]:
            raise SystemExit(f"{msg} '{c.SENS_GEOM}' cannot be empty")
        if c.CLS not in sensor_data[c.SENS_GEOM] or c.KW not in sensor_data[c.SENS_GEOM]:
            raise SystemExit(f"{msg} '{c.SENS_GEOM}' must have '{c.CLS}' and '{c.KW}' keys")
