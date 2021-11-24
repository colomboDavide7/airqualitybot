######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 09:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.database.record.baserec as base
import airquality.database.util.datatype.timestamp as ts
import airquality.adapter.api2db.updtadapt.updtadapt as updtadapt


class UpdateRecord(base.BaseRecord):

    def __init__(self, sensor_at_loc_values: str, current_timestamp=ts.CurrentTimestamp()):
        self.sensor_at_loc_values = sensor_at_loc_values
        self.current_timestamp = current_timestamp


class UpdateRecordBuilder(base.BaseRecordBuilder):

    def record(self, sensor_data: List[updtadapt.UpdateUniformModel], sensor_id: int = None) -> UpdateRecord:
        sensor_at_loc_values = ""

        for data in sensor_data:
            g = data.geolocation
            sensor_at_loc_values += f"({sensor_id}, '{g.timestamp.get_formatted_timestamp()}', {g.geolocation.geom_from_text()}),"

        return UpdateRecord(sensor_at_loc_values=sensor_at_loc_values)
