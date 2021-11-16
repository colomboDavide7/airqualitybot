######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any


class RecordBuilder(abc.ABC):

    @abc.abstractmethod
    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        pass

    @abc.abstractmethod
    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        pass
