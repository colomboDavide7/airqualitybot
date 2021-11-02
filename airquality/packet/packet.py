######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 16:06
# Description: this script defines the classes for the packet hierarchy
#
######################################################
from abc import ABC, abstractmethod


class Packet(ABC):

    @abstractmethod
    def sql(self) -> str:
        pass
