######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 11:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import database.record.baserec as base
import airquality.adapter.config as adapt_const


class TimeRecord(base.BaseRecordBuilder):

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)

        timestamp_class = sensor_data[adapt_const.TIMEST][adapt_const.CLS]
        class_kwargs = sensor_data[adapt_const.TIMEST][adapt_const.KW]
        return f"'{timestamp_class(**class_kwargs).get_formatted_timestamp()}'"

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        msg = f"{TimeRecord.__name__}: bad sensor data =>"

        if adapt_const.TIMEST not in sensor_data:
            raise SystemExit(f"{msg} missing key='{adapt_const.TIMEST}'")
        if not sensor_data[adapt_const.TIMEST]:
            raise SystemExit(f"{msg} '{adapt_const.TIMEST}' cannot be empty")
        if adapt_const.CLS not in sensor_data[adapt_const.TIMEST] or adapt_const.KW not in sensor_data[adapt_const.TIMEST]:
            raise SystemExit(f"{msg} '{adapt_const.TIMEST}' must have '{adapt_const.CLS}' and '{adapt_const.KW}' keys")
