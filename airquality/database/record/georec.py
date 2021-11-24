######################################################
#
# Author: Davide Colombo
# Date: 18/11/21 14:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import database.record.baserec as base
import airquality.adapter.config as adapt_const


class LocationRecord(base.BaseRecordBuilder):

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data=sensor_data)

        postgis_class = sensor_data[adapt_const.SENS_GEOM][adapt_const.CLS]
        class_kwargs = sensor_data[adapt_const.SENS_GEOM][adapt_const.KW]
        return postgis_class(**class_kwargs).geom_from_text()

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        msg = f"{LocationRecord.__name__} bad sensor data =>"

        if adapt_const.SENS_GEOM not in sensor_data:
            raise SystemExit(f"{msg} missing key='{adapt_const.SENS_GEOM}'")
        if not sensor_data[adapt_const.SENS_GEOM]:
            raise SystemExit(f"{msg} '{adapt_const.SENS_GEOM}' cannot be empty")
        if adapt_const.CLS not in sensor_data[adapt_const.SENS_GEOM] or adapt_const.KW not in sensor_data[adapt_const.SENS_GEOM]:
            raise SystemExit(f"{msg} '{adapt_const.SENS_GEOM}' must have '{adapt_const.CLS}' and '{adapt_const.KW}' keys")
