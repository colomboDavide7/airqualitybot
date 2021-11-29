######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 12:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.loggable as log
import airquality.types.timestamp as ts
import airquality.types.postgis as pgis


class MeasureRecordBuilder(log.Loggable, abc.ABC):

    def __init__(self, log_filename="log"):
        super(MeasureRecordBuilder, self).__init__(log_filename=log_filename)
        self.name2id = None
        self.sensor_id = None

    @abc.abstractmethod
    def get_measure_value(self, record_id: int, timestamp: ts.Timestamp, param_name: str, param_value: str) -> str:
        pass


################################ MOBILE MEASURE RECORD ################################
class MobileRecordBuilder(MeasureRecordBuilder):

    def __init__(self, log_filename="log"):
        super(MobileRecordBuilder, self).__init__(log_filename=log_filename)
        self.geom: pgis.PostgisGeometry = pgis.NullGeometry()

    def with_geometry(self, geom: pgis.PostgisGeometry):
        self.geom = geom
        return self

    def get_measure_value(self, record_id: int, timestamp: ts.Timestamp, param_name: str, param_value: str) -> str:
        geometry = self.geom.geom_from_text()
        fmt_ts = timestamp.get_formatted_timestamp()
        param_id = self.name2id[param_name]

        return f"({record_id}, {param_id}, '{param_value}', '{fmt_ts}', {geometry})" if param_value is not None \
            else f"({record_id}, {param_id}, NULL, '{fmt_ts}', {geometry})"


################################ STATION MEASURE RECORD ################################
class StationRecordBuilder(MeasureRecordBuilder):

    def __init__(self, log_filename="log"):
        super(StationRecordBuilder, self).__init__(log_filename=log_filename)

    def get_measure_value(self, record_id: int, timestamp: ts.Timestamp, param_name: str, param_value: str) -> str:
        fmt_ts = timestamp.get_formatted_timestamp()
        param_id = self.name2id[param_name]
        return f"({record_id}, {param_id}, {self.sensor_id}, '{param_value}', '{fmt_ts}')" if param_value is not None \
            else f"({record_id}, {param_id}, {self.sensor_id}, NULL, '{fmt_ts}')"
