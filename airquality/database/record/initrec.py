######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 08:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.database.record.baserec as base
import airquality.adapter.api2db.initadapt.initadapt as initadpt


class InitRecord(base.BaseRecord):

    def __init__(self, sensor_values: str, api_param_values: str, channel_info_values: str, sensor_at_loc_values: str):
        self.sensor_value = sensor_values
        self.api_param_values = api_param_values
        self.channel_info_values = channel_info_values
        self.sensor_at_loc_values = sensor_at_loc_values


class InitRecordBuilder(base.BaseRecordBuilder):

    def record(self, sensor_data: List[initadpt.InitUniformModel], sensor_id: int = None) -> InitRecord:
        sensor_values = ""
        api_param_values = ""
        channel_info_values = ""
        sensor_at_loc_values = ""

        for data in sensor_data:
            sensor_values += f"({sensor_id}, '{data.type}', '{data.name}'),"
            for p in data.parameters:
                api_param_values += f"({sensor_id}, '{p.name}', '{p.value}'),"
            for c in data.channels:
                channel_info_values += f"({sensor_id}, '{c.name}', '{c.timestamp.get_formatted_timestamp()}'),"
            g = data.geolocation
            sensor_at_loc_values += f"({sensor_id}, '{g.timestamp.get_formatted_timestamp()}', {g.geolocation.geom_from_text()}),"

        return InitRecord(
            sensor_values=sensor_values,
            api_param_values=api_param_values,
            channel_info_values=channel_info_values,
            sensor_at_loc_values=sensor_at_loc_values
        )
