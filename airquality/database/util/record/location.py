######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 10:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.database.util.record.base as base
import airquality.database.util.postgis.geom as postgis


class LocationRecord(base.RecordBuilder):

    def __init__(self, postgis_builder: postgis.GeometryBuilder):
        self.postgis_builder = postgis_builder

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        return f"{self.postgis_builder.geom_from_text(sensor_data)}"

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        pass
