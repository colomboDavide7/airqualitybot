######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 09:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.database.record.baserec as base
import airquality.database.util.datatype.timestamp as ts
import airquality.adapter.api2db.updtadapt.updtadapt as updtadapt


class UpdateRecord(base.BaseRecord):

    def __init__(self, sensor_at_loc_values: str, update_info: base.ParamIDTimestamp):
        self.sensor_at_loc_values = sensor_at_loc_values
        self.update_info = update_info


class UpdateRecordBuilder(base.BaseRecordBuilder):

    def record(self, sensor_data: updtadapt.UpdateUniformModel, sensor_id: int) -> UpdateRecord:
        g = sensor_data.geolocation

        return UpdateRecord(
            sensor_at_loc_values=f"({sensor_id}, '{g.timestamp.get_formatted_timestamp()}', {g.geolocation.geom_from_text()}),",
            update_info=base.ParamIDTimestamp(sensor_id=sensor_id, timestamp=ts.CurrentTimestamp())
        )
