######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.adapter.api2db.baseadpt as baseadpt


class BaseRecord:
    pass


class BaseRecordBuilder(abc.ABC):

    @abc.abstractmethod
    def record(self, sensor_data: List[baseadpt.BaseUniformModel], sensor_id: int = None) -> BaseRecord:
        pass
