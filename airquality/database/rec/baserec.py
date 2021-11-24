######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.api2db.baseunif as baseunif
import airquality.database.dtype.timestamp as ts


class ParamIDTimestamp:

    def __init__(self, sensor_id: int, timestamp: ts.Timestamp):
        self.id = sensor_id
        self.timestamp = timestamp


class BaseRecord:
    pass


class BaseRecordBuilder(abc.ABC):

    @abc.abstractmethod
    def record(self, uniform_response: baseunif.BaseUniformResponse, sensor_id: int) -> BaseRecord:
        pass
