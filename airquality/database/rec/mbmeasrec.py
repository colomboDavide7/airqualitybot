######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 15:20
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.api2db.adptype as adptype


class MobileMeasureRecord:

    def __init__(self, record_id: int, mb_meas: adptype.MobileMeasure):
        self.rec_id = record_id
        self.mb_meas = mb_meas

    def get_mobile_measurement_value(self) -> str:
        fmt_ts = self.mb_meas.timestamp.get_formatted_timestamp()
        geom = self.mb_meas.geometry.geom_from_text()
        return ','.join(f"({self.rec_id}, {m.param_id}, '{m.param_val}', '{fmt_ts}', {geom})" for m in self.mb_meas.measures)
