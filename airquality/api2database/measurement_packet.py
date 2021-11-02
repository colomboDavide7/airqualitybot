######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 11:34
# Description: this script defines a class that is used for communication between API and database.
#
######################################################
import builtins


class MobileMeasurementPacket(builtins.object):

    def __init__(self, param_id: int, param_val: str, timestamp: str, geom: str):
        super().__init__()
        self.param_id = param_id
        self.param_val = param_val
        self.timestamp = timestamp
        self.geom = geom

    def __eq__(self, other):
        if not isinstance(other, MobileMeasurementPacket):
            raise SystemExit(f"{MobileMeasurementPacket.__name__}: 'other' argument is not instance of the same class.")

        return other.param_id == self.param_id and other.param_val == self.param_val and \
            other.geom == self.geom and other.timestamp == self.timestamp

    def __str__(self):
        return f"param_id={self.param_id}, param_va={self.param_val}, timestamp={self.timestamp}, geom={self.geom}"


class StationMeasurementPacket(builtins.object):

    def __init__(self, param_id: int, sensor_id: int, param_val: str, timestamp: str):
        super().__init__()
        self.param_id = param_id
        self.sensor_id = sensor_id
        self.param_val = param_val
        self.timestamp = timestamp

    def __eq__(self, other):
        if not isinstance(other, StationMeasurementPacket):
            raise SystemExit(f"{StationMeasurementPacket.__name__}: 'other' argument is not instance of the same class.")

        return other.param_id == self.param_id and other.param_val == self.param_val and \
            other.sensor_id == self.sensor_id and other.timestamp == self.timestamp

    def __str__(self):
        return f"param_id={self.param_id}, param_va={self.param_val}, timestamp={self.timestamp}, sensor_id={self.sensor_id}"
