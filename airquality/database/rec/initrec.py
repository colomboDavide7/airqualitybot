######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 08:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.database.rec.baserec as baserec
import airquality.api2db.initunif.initunif as initunif


class InitRecord(baserec.BaseRecord):

    def __init__(self, sensor_value: str, api_param_value: str, channel_info_value: str, sensor_at_loc_value: str):
        self.sensor_value = sensor_value
        self.api_param_value = api_param_value
        self.channel_info_value = channel_info_value
        self.sensor_at_loc_value = sensor_at_loc_value


class InitRecordBuilder(baserec.BaseRecordBuilder):

    def record(self, uniformed_responses: initunif.InitUniformResponse, sensor_id: int) -> InitRecord:
        g = uniformed_responses.geolocation
        channel_info_values = ','.join(f"({sensor_id}, '{c.name}', '{c.timestamp.get_formatted_timestamp()}')"
                                       for c in uniformed_responses.channels) + ','
        return InitRecord(
            sensor_value=f"({sensor_id}, '{uniformed_responses.type}', '{uniformed_responses.name}'),",
            api_param_value=','.join(f"({sensor_id}, '{p.name}', '{p.value}')" for p in uniformed_responses.parameters) + ',',
            channel_info_value=channel_info_values,
            sensor_at_loc_value=f"({sensor_id}, '{g.timestamp.get_formatted_timestamp()}', {g.geometry.geom_from_text()}),"
        )
