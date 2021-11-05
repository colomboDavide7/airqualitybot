######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 11:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC
from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class InitializeContainer(ABC):
    database_sensor_name: str = field(init=False)


@dataclass
class InitializeContainerPurpleair(InitializeContainer):
    name: str
    sensor_index: str
    primary_id_a: str
    primary_id_b: str
    secondary_id_a: str
    secondary_id_b: str
    primary_key_a: str
    primary_key_b: str
    secondary_key_a: str
    secondary_key_b: str
    latitude: str
    longitude: str
    altitude: str

    def __post_init__(self):
        self.database_sensor_name = f"{self.name} ({self.sensor_index})"


################################ CONTAINER FACTORY ################################
class InitializeContainerFactory:

    @staticmethod
    def make_container(bot_personality: str, parameters: Dict[str, Any]) -> InitializeContainer:
        if bot_personality == 'purpleair':
            return InitializeContainerPurpleair(**parameters)
        else:
            raise SystemExit(f"{InitializeContainerFactory.__name__}: cannot instantiate {InitializeContainer.__name__} "
                             f"instance for personality='{bot_personality}'.")
