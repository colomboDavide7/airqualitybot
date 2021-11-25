######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 15:17
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.api2db.adptype as adptype


class StationMeasureRecord:

    def __init__(self, st_meas: adptype.StationMeasure, sensor_id: int, record_id: int):
        self.st_meas = st_meas
        self.sensor_id = sensor_id
        self.rec_id = record_id

    def get_station_measurement_value(self) -> str:
        fmt_ts = self.st_meas.timestamp.get_formatted_timestamp()
        return ','.join(f"({self.rec_id}, {m.param_id}, {self.sensor_id}, '{m.param_val}', {fmt_ts})" for m in self.st_meas.measures)
