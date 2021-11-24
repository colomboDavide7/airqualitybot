######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.adapter.api2db.baseadpt as baseadpt
import airquality.database.util.datatype.timestamp as ts


class ParamIDTimestamp:

    def __init__(self, sensor_id: int, timestamp: ts.Timestamp):
        self.id = sensor_id
        self.timestamp = timestamp


class BaseRecord:
    pass


class BaseRecordBuilder(abc.ABC):

    @abc.abstractmethod
    def record(self, sensor_data: baseadpt.BaseUniformModel, sensor_id: int) -> BaseRecord:
        pass
