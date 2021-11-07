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
from airquality.constants.shared_constants import EXCEPTION_HEADER


class SensorAdapter(ABC):

    @abstractmethod
    def adapt(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        pass


class SensorAdapterPurpleair(SensorAdapter):

    def adapt(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        keys = packet.keys()
        if 'name' not in keys or 'sensor_index' not in keys:
            raise SystemExit(f"{EXCEPTION_HEADER} {SensorAdapterPurpleair.__name__} missing keys=['name' | 'sensor_index'].")

        return {'name': f"{packet['name']} ({packet['sensor_index']})"}


class SensorAdapterFactory:

    def __init__(self, sensor_adapter_class=SensorAdapter):
        self.sensor_adapter_class = sensor_adapter_class

    def make_adapter(self) -> SensorAdapter:
        return self.sensor_adapter_class()
