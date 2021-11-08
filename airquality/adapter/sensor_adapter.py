######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 19:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC, abstractmethod
from typing import Dict, Any
from airquality.container.sql_container import SensorSQLContainer
from airquality.constants.shared_constants import EXCEPTION_HEADER


class SensorAdapter(ABC):

    @abstractmethod
    def adapt(self, packet: Dict[str, Any]) -> SensorSQLContainer:
        pass


class SensorAdapterPurpleair(SensorAdapter):

    def adapt(self, packet: Dict[str, Any]) -> SensorSQLContainer:
        keys = packet.keys()
        if 'name' not in keys or 'sensor_index' not in keys:
            raise SystemExit(f"{EXCEPTION_HEADER} {SensorAdapterPurpleair.__name__} missing keys=['name' | 'sensor_index'].")
        return SensorSQLContainer(name=f"{packet['name']} ({packet['sensor_index']})", type_='purpleair')
