######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 10:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
from airquality.container.container import \
    PurpleairGeolocationContainer, PurpleairAPIParamContainer, PurpleairSensorContainer, PurpleairContainer


class ContainerFactory(ABC):

    @abstractmethod
    def make_container(self, packet: Dict[str, Any]):
        pass


@dataclass
class PurpleairContainerFactory(ContainerFactory):
    sensor_id: int

    def make_container(self, packet: Dict[str, Any]) -> PurpleairContainer:

        # api param
        api_param_container = PurpleairAPIParamContainer(primary_id_a=packet['primary_id_a'],
                                                         primary_id_b=packet['primary_id_b'],
                                                         secondary_id_a=packet['secondary_id_a'],
                                                         secondary_id_b=packet['secondary_id_b'],
                                                         primary_key_a=packet['primary_key_a'],
                                                         primary_key_b=packet['primary_key_b'],
                                                         secondary_key_a=packet['secondary_key_a'],
                                                         secondary_key_b=packet['secondary_key_b'],
                                                         sensor_id=self.sensor_id)
        # sensor
        sensor_container = PurpleairSensorContainer(name=packet['name'],
                                                    sensor_index=packet['sensor_index'])

        # geolocation
        geolocation_container = PurpleairGeolocationContainer(latitude=packet['latitude'],
                                                              longitude=packet['longitude'],
                                                              sensor_id=self.sensor_id)

        # container
        container = PurpleairContainer(sensor=sensor_container,
                                       api_param=api_param_container,
                                       geolocation=geolocation_container)
        return container
