######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 09:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.database.rec.baserec as base
import airquality.database.dtype.timestamp as ts
import airquality.api2db.updtunif.updtunif as updtunif


class UpdateRecord(base.BaseRecord):

    def __init__(self, sensor_at_loc_values: str, update_info: base.ParamIDTimestamp):
        self.sensor_at_loc_values = sensor_at_loc_values
        self.update_info = update_info


class UpdateRecordBuilder(base.BaseRecordBuilder):

    def record(self, uniform_response: updtunif.UpdateUniformResponse, sensor_id: int) -> UpdateRecord:
        g = uniform_response.geolocation

        return UpdateRecord(
            sensor_at_loc_values=f"({sensor_id}, '{g.timestamp.get_formatted_timestamp()}', {g.geometry.geom_from_text()}),",
            update_info=base.ParamIDTimestamp(sensor_id=sensor_id, timestamp=ts.CurrentTimestamp())
        )
