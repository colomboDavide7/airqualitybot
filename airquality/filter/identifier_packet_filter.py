#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 12:20
# @Description: this script defines the classes for filtering packets coming from sensor's API based on some criteria
#
#################################################
import builtins
from abc import ABC, abstractmethod
from typing import List
from airquality.plain.plain_api_packet import PlainAPIPacketPurpleair, PlainAPIPacket
from airquality.constants.shared_constants import EMPTY_LIST
from airquality.container.initialize_container import InitializeContainer

# class IdentifierPacketFilter(ABC):
#     """Abstract Base Class that defines an abstract method for filtering API answer packets based on a sensor identifier.
#
#     This can be useful to check whether a given sensor is already present in the database or not."""
#
#     @abstractmethod
#     def filter_packets(self, packets: List[PlainAPIPacket], identifiers: List[str]) -> List[PlainAPIPacket]:
#         pass


class ContainerIdentifierFilter:

    @staticmethod
    def filter_packets(containers: List[InitializeContainer], identifiers: List[str]) -> List[InitializeContainer]:

        if identifiers == EMPTY_LIST:
            return containers

        filtered_containers = []
        for container in containers:
            if container.database_sensor_name not in identifiers:
                filtered_containers.append(container)
        return filtered_containers


################################ FACTORY ################################
# class IdentifierPacketFilterFactory(builtins.object):
#
#     @classmethod
#     def create_identifier_filter(cls, bot_personality: str) -> IdentifierPacketFilter:
#
#         if bot_personality == "purpleair":
#             return IdentifierPacketFilterPurpleair()
#         else:
#             raise SystemExit(
#                 f"{IdentifierPacketFilterFactory.__name__}: cannot instantiate {IdentifierPacketFilter.__name__} "
#                 f"instance for personality='{bot_personality}'.")
